from __future__ import annotations

import argparse
import io
import os
import platform
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.dom import minidom
import xml.etree.ElementTree as XmlTree

from lxml import etree as ET
from pcpp import Action, OutputDirective, Preprocessor
from pycparser import CParser
from saxonche import PySaxonProcessor


ROOT_DIR = Path(__file__).resolve().parent
CACHE_DIR = ROOT_DIR / ".smv_cache"
SENTINEL = "zz0912819zz"
XSLT_CHAIN = [
    "s00005_identity.xml",
    "s00100_declutter_attributes.xml",
    "s00200_add_bLine_eLine.xml",
    "s00300_add_CurrentStateTest.xml",
    "s00300_add_EventParamTest.xml",
    "s00300_add_EventTypeTest.xml",
    "s00300_add_NextStateLabel.xml",
    "s00400_add_CascadeElements.xml",
    "s00500_add_CascadeLabel.xml",
    "s00550_add_EventLabel.xml",
    "s00560_add_Guard_Element.xml",
    "s00570_add_Guard_Attributes.xml",
    "s00600_add_onEntry_onExit.xml",
    "s00600_add_onTransition2.xml",
    "s00620_drop_unwanted_code.xml",
]
FINAL_XSLT = "s00800_gv_digraph4.xml"
SOURCE_SUFFIXES = {".c", ".h", ".hpp"}
ENCODING = "utf-8"
FRAMEWORK_ROOT_ENV = "SMV_FRAMEWORK_ROOT"
PIC32_INCLUDE_ENV = "SMV_PIC32_INCLUDE"
GRAPHVIZ_DOT_ENV = "SMV_DOT"
GVEDIT_ENV = "SMV_GVEDIT"

XSLT_ASSETS = {
    's00005_identity.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    \n    <xsl:strip-space elements="*" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n',
    's00100_declutter_attributes.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<!-- \n\nDrop attributes known not to be useful.\n\nDrop attributes that are empty strings.\n    \n-->\n<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n  <xsl:template match="@quals"/>\n  <xsl:template match="@align"/>\n  <xsl:template match="@storage"/>\n  <xsl:template match="@funcspec"/>\n  <xsl:template match="@line[.=\'None\']"/>\n  \n  <xsl:template match="@*[normalize-space(.)=\'\']"/>\n\n  <!-- identity transform - copy all input nodes to output -->\n  <xsl:template match="@*|node()" >\n    <xsl:copy>\n      <xsl:apply-templates select="@*|node()"/>\n    </xsl:copy>\n  </xsl:template>\n\n</xsl:stylesheet>\n',
    's00200_add_bLine_eLine.xml': '<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n  <!-- Identity transform template -->\n  <xsl:template match="@*|node()">\n    <xsl:copy>\n      <xsl:apply-templates select="@*|node()"/>\n    </xsl:copy>\n  </xsl:template>\n\n  <!-- Add "endline" attribute to each node with the maximum "line" value of its children -->\n  <xsl:template match="*[@line and @line!=\'None\' and .//*[@line] ]">\n    <xsl:copy>\n      <xsl:apply-templates select="@*"/>\n      <xsl:attribute name="bLine">\n        <xsl:value-of select="min(descendant-or-self::*/@line)"/>\n      </xsl:attribute>\n      <xsl:attribute name="eLine">\n        <xsl:value-of select="max(descendant-or-self::*/@line)"/>\n      </xsl:attribute>\n      <xsl:apply-templates select="node()"/>\n    </xsl:copy>\n  </xsl:template>\n</xsl:stylesheet>\n',
    's00300_add_CurrentStateTest.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<!-- \n\n    TODO CurrentState If \n\n\n-->\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n    \n    <!-- CurrentState Switch\n\n        <block_items class="Switch" line="616" blockbegin="616" blockend="736">\n            <cond class="ID" line="616" name="CurrentState"/>\n            <stmt class="Compound" line="616" blockbegin="616" blockend="736">\n                <block_items class="Case" line="617" blockbegin="617" blockend="624"\n                            CurrentStateTest="InitPSubState">\n                    <expr class="ID" line="617" name="InitPSubState"/>\n    \n     -->\n    <xsl:template match="\n        block_items[\n            (@class=\'Case\' \n                or @class=\'Default\')\n            and (\n                ../../..\n                /block_items[@class=\'Switch\']\n                /cond[@class=\'ID\' and @name=\'CurrentState\']\n            )\n            and not(@CurrentStateTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="CurrentStateTest">\n                <xsl:value-of select="./expr[@class=\'ID\']/@name"/>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n\n</xsl:stylesheet>\n',
    's00300_add_EventParamTest.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n    \n    <!-- EventParam Switch\n    \n    \n     -->\n    <xsl:template match="\n        block_items[\n            (@class=\'Case\' \n                or @class=\'Default\'\n            )\n            and ../../..\n                /*[@class=\'Switch\']\n                /cond\n                //field[@class=\'ID\' and @name=\'EventParam\']\n            and not(@EventParamTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventParamTest">\n                <xsl:value-of select="./expr[@class=\'ID\']/@name"/>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <!-- EventParam If\n    \n        <stmts class="If" line="696" blockbegin="696" blockend="717" EventParamTest="">\n            <cond class="BinaryOp" line="696" op="==" blockbegin="696" blockend="696">\n            <left class="StructRef" line="696" type="." blockbegin="696" blockend="696">\n                <name class="ID" line="696" name="ThisEvent"/>\n                <field class="ID" line="696" name="EventParam"/>\n            </left>\n            <right class="Constant" line="696" type="int" value="1"/>\n            </cond>\n    \n     -->\n    <!-- <xsl:template match="\n        *[\n            @class=\'If\'\n            and ./cond\n                //field[\n                    @class=\'ID\' and @name=\'EventParam\'\n                ]\n            and not(@EventParamTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventParamTest">\n                <xsl:for-each select=" \n                    ./cond\n                    //*[\n                        @class=\'StructRef\' \n                        and ./field[\n                            @class=\'ID\' and @name=\'EventParam\'\n                        ]\n                    ]\n                    /..\n                    /*[@class=\'ID\' or @class=\'Constant\']\n                ">\n                    <xsl:value-of select="@name"/>\n                    <xsl:value-of select="@value"/>\n                </xsl:for-each>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template> -->\n\n    <xsl:template match="\n        iftrue[\n            ../cond\n                //field[\n                    @class=\'ID\' and @name=\'EventParam\'\n                ]\n            and not(@EventParamTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventParamTest">\n                <xsl:for-each select=" \n                    ../cond\n                    //*[\n                        @class=\'StructRef\' \n                        and ./field[\n                            @class=\'ID\' and @name=\'EventParam\'\n                        ]\n                    ]\n                    /..\n                    /*[@class=\'ID\' or @class=\'Constant\']\n                ">\n                    <xsl:value-of select="@name"/>\n                    <xsl:value-of select="@value"/>\n                </xsl:for-each>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n\n\n<!-- \n<iffalse class="If" line="705" bLine="705" eLine="717" EventParamTest="2">\n    <cond class="BinaryOp" line="705" op="==" bLine="705" eLine="705">\n        <left class="StructRef" line="705" type="." bLine="705" eLine="705">\n            <name class="ID" line="705" name="ThisEvent"></name>\n            <field class="ID" line="705" name="EventParam"></field>\n        </left>\n        <right class="Constant" line="705" type="int" value="2"></right>\n    </cond>\n    <iftrue class="Compound" line="706" bLine="706" eLine="712">\n        <block_items class="Assignment" line="707" op="=" bLine="707" eLine="707">\n            <lvalue class="ID" line="707" name="previousBumpers"></lvalue>\n            <rvalue class="Constant" line="707" type="int" value="2"></rvalue>\n        </block_items>\n        <block_items class="FuncCall" line="708" bLine="708" eLine="708">\n            <name class="ID" line="708" name="backUpLeft"></name>\n            <args class="ExprList" line="708" bLine="708" eLine="708">\n                <exprs class="Constant" line="708" type="int" value="90"></exprs>\n            </args>\n        </block_items>\n        <block_items class="FuncCall" line="709" bLine="709" eLine="709">\n            <name class="ID" line="709" name="ES_Timer_InitTimer"></name>\n            <args class="ExprList" line="709" bLine="709" eLine="709">\n                <exprs class="Constant" line="709" type="int" value="0"></exprs>\n                <exprs class="Constant" line="709" type="int" value="3000"></exprs>\n            </args>\n        </block_items>\n        <block_items class="Assignment" line="710" op="=" bLine="710" eLine="710" NextStateLabel="Getting_Unstuck" EventLabel="(FRONT_RIGHT_BUMPER_PRESSED or FRONT_LEFT_BUMPER_PRESSED)(2)">\n            <lvalue class="ID" line="710" name="nextState"></lvalue>\n            <rvalue class="ID" line="710" name="Getting_Unstuck"></rvalue>\n        </block_items>\n        <block_items class="Assignment" line="711" op="=" bLine="711" eLine="711">\n            <lvalue class="ID" line="711" name="makeTransition"></lvalue>\n            <rvalue class="ID" line="711" name="TRUE"></rvalue>\n        </block_items>\n        <block_items class="Assignment" line="712" op="=" bLine="712" eLine="712">\n            <lvalue class="StructRef" line="712" type="." bLine="712" eLine="712">\n                <name class="ID" line="712" name="ThisEvent"></name>\n                <field class="ID" line="712" name="EventType"></field>\n            </lvalue>\n            <rvalue class="ID" line="712" name="ES_NO_EVENT"></rvalue>\n        </block_items>\n    </iftrue>\n    <iffalse class="Compound" line="714" bLine="714" eLine="717">\n        <block_items class="Assignment" line="715" op="=" bLine="715" eLine="715" NextStateLabel="Reversing" \n            EventLabel="(FRONT_RIGHT_BUMPER_PRESSED or FRONT_LEFT_BUMPER_PRESSED)(2)">\n            <lvalue class="ID" line="715" name="nextState"></lvalue>\n            <rvalue class="ID" line="715" name="Reversing"></rvalue>\n        </block_items>\n        <block_items class="Assignment" line="716" op="=" bLine="716" eLine="716">\n            <lvalue class="ID" line="716" name="makeTransition"></lvalue>\n            <rvalue class="ID" line="716" name="TRUE"></rvalue>\n        </block_items> -->',
    's00300_add_EventTypeTest.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <!-- EventType Switch \n\n        <stmts class="Switch" line="626" blockbegin="626" blockend="640">\n            <cond class="StructRef" line="626" type="." blockbegin="626" blockend="626">\n                <name class="ID" line="626" name="ThisEvent"/>\n                <field class="ID" line="626" name="EventType"/>\n            </cond>\n    \n    -->\n    <xsl:template match="\n        block_items[\n            (@class=\'Case\' \n                or @class=\'Default\'\n            )\n            and ../../..\n                /*[@class=\'Switch\']\n                /cond\n                //field[@class=\'ID\' and @name=\'EventType\']\n            and not(@EventTypeTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventTypeTest">\n                <xsl:value-of select="./expr[@class=\'ID\']/@name"/>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <!-- EventType If \n    \n        <stmts class="If" line="618" blockbegin="618" blockend="622" EventTypeTest="ES_INIT">\n            <cond class="BinaryOp" line="618" op="==" blockbegin="618" blockend="618">\n                <left class="StructRef" line="618" type="." blockbegin="618" blockend="618">\n                    <name class="ID" line="618" name="ThisEvent"/>\n                    <field class="ID" line="618" name="EventType"/>\n                </left>\n                <right class="ID" line="618" name="ES_INIT"/>\n            </cond>\n            <iftrue class="Compound" line="619" blockbegin="619" blockend="622">\n                <block_items class="Assignment" line="620" op="=" blockbegin="620" blockend="620">\n                    <lvalue class="ID" line="620" name="nextState"/>\n                    <rvalue class="ID" line="620" name="Hiding"/>\n                </block_items>\n    \n    -->\n<!-- \n    <xsl:template match="\n        stmts[\n            @class=\'If\'\n            and ./cond\n                //field[\n                    @class=\'ID\' and @name=\'EventType\'\n                ]\n            and not(@EventTypeTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventTypeTest">\n                <xsl:for-each select=" \n                    ./cond\n                    //*[\n                        @class=\'StructRef\' \n                        and ./field[\n                            @class=\'ID\' and @name=\'EventType\'\n                        ]\n                    ]\n                    /..\n                    /*[@class=\'ID\' or @class=\'Constant\']\n                ">\n                    <xsl:value-of select="@name"/>\n                    <xsl:value-of select="@value"/>\n                </xsl:for-each>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template> -->\n\n\n    <xsl:template match="\n        iftrue[\n            ../cond\n                //field[\n                    @class=\'ID\' and @name=\'EventType\'\n                ]\n            and not(@EventTypeTest)\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="EventTypeTest">\n                <xsl:for-each select=" \n                    ../cond\n                    //*[\n                        @class=\'StructRef\' \n                        and ./field[\n                            @class=\'ID\' and @name=\'EventType\'\n                        ]\n                    ]\n                    /..\n                    /*[@class=\'ID\' or @class=\'Constant\']\n                ">\n                    <xsl:value-of select="@name"/>\n                    <xsl:value-of select="@value"/>\n                </xsl:for-each>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n',
    's00300_add_NextStateLabel.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <!-- annotate state change -->\n    <xsl:template match="\n            *[\n                @class=\'Assignment\'\n                and @op=\'=\'\n                    and lvalue[@name=\'nextState\']\n            ]\n        ">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name="NextStateLabel">\n                <xsl:value-of select="./rvalue/@name"/>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n',
    's00400_add_CascadeElements.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n\n    <!-- Handle first case with a break within a block \n            \n    -->\n    <xsl:template match="\n        block_items[\n            (@class=\'Case\' \n            or @class=\'Default\')\n            and not(\n                preceding-sibling::block_items[\n                    @class=\'Case\'\n                ]\n                /stmts[\n                    @class=\'Break\'\n                ]\n            )\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n\n            <xsl:for-each select=" \n                preceding-sibling::block_items[\n                    @class=\'Case\'\n                    and not(\n                        stmts[\n                            @class=\'Break\'\n                        ]\n                    )\n                ]\n            ">\n                <xsl:element name="CascadeElement">\n                    <xsl:attribute name="name">\n                        <xsl:value-of select="./expr[@class=\'ID\']/@name"/>\n                    </xsl:attribute>\n                </xsl:element>\n            </xsl:for-each>\n\n            <xsl:apply-templates select="node()"/>\n\n        </xsl:copy>\n    </xsl:template>\n\n    <!-- Handle any case with a break when it is preceeded by a case with a break \n    \n    -->\n    <xsl:template match="\n        block_items[\n            (@class=\'Case\' \n            or @class=\'Default\')\n            and (\n                preceding-sibling::block_items[\n                    @class=\'Case\'\n                ]\n                /stmts[\n                    @class=\'Break\'\n                ]\n            )\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:for-each select=" \n                    preceding-sibling::block_items[\n                        @class=\'Case\'\n                        and stmts[ @class=\'Break\' ]\n                    ][1]/following-sibling::block_items[\n                        @class=\'Case\'\n                        and not(\n                            stmts[\n                                @class=\'Break\'\n                            ]\n                        )\n                    ]\n                intersect\n                    preceding-sibling::block_items[\n                        @class=\'Case\'\n                        and not(\n                            stmts[\n                                @class=\'Break\'\n                            ]\n                        )\n                    ]\n            ">\n                <xsl:element name="CascadeElement">\n                    <xsl:attribute name="name">\n                        <xsl:value-of select="./expr[@class=\'ID\']/@name"/>\n                    </xsl:attribute>\n                </xsl:element>\n            </xsl:for-each>\n\n            <xsl:apply-templates select="node()"/>\n\n        </xsl:copy>\n    </xsl:template>\n\n    \n\n\n</xsl:stylesheet>\n',
    's00500_add_CascadeLabel.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<!--\n\nLabel case cascades such as for FRONT_LEFT_BUMPER_PRESSED below:\n\n          //Handle front bumpers\n        case FRONT_LEFT_BUMPER_PRESSED:\n        case FRONT_RIGHT_BUMPER_PRESSED:\n            nextState = Reversing;\n            makeTransition = TRUE;\n            ThisEvent.EventType = ES_NO_EVENT;\n            break;\n\n  ** INPUT and OUTPUT samples are supplied at the end of this file.**\n\n-->\n<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n  <xsl:template\n    match="\n      block_items[\n        @class=\'Case\'\n        and not(@CascadeLabel)\n      ]\n    ">\n    <xsl:copy>\n      <xsl:apply-templates select="@*" />\n      <xsl:attribute name="CascadeLabel">\n        <xsl:value-of select="expr[@class=\'ID\']/@name" />\n        <xsl:for-each select="CascadeElement">\n            <xsl:text> or </xsl:text>\n            <xsl:value-of select="@name" />\n        </xsl:for-each>\n      </xsl:attribute>       \n      <xsl:apply-templates select="node()" />\n    </xsl:copy>\n  </xsl:template>\n\n  <!-- identity transform - copy all input nodes to output -->\n  <xsl:template match="@*|node()">\n    <xsl:copy>\n      <xsl:apply-templates select="@*|node()" />\n    </xsl:copy>\n  </xsl:template>\n\n</xsl:stylesheet>\n\n<!--\n\nSample FSM C code INPUT:\n\n      case Driving:\n        switch (ThisEvent.EventType) {\n... \n        //Handle front bumpers\n        case FRONT_LEFT_BUMPER_PRESSED:\n        case FRONT_RIGHT_BUMPER_PRESSED:\n            nextState = Reversing;\n            makeTransition = TRUE;\n            ThisEvent.EventType = ES_NO_EVENT;\n            break;\n...\n\n\nSample Abstract Syntax Tree INPUT\n\n                <block_items class="Case">\n                  <expr class="ID" name="REAR_LEFT_BUMPER_PRESSED"/>\n                </block_items>\n                <block_items class="Case">\n                  <expr class="ID" name="REAR_RIGHT_BUMPER_PRESSED"/>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="ID" name="nextState"/>\n                    <rvalue class="ID" name="Driving"/>\n                  </stmts>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="ID" name="makeTransition"/>\n                    <rvalue class="ID" name="TRUE"/>\n                  </stmts>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="StructRef" type=".">\n                      <name class="ID" name="ThisEvent"/>\n                      <field class="ID" name="EventType"/>\n                    </lvalue>\n                    <rvalue class="ID" name="ES_NO_EVENT"/>\n                  </stmts>\n                  <stmts class="Break"/>\n                </block_items>\n  \nSample Abstract Syntax Tree OUTPUT\n\n                <block_items class="Case" CascadeLabel="REAR_LEFT_BUMPER_PRESSED" >\n                  <expr class="ID" name="REAR_LEFT_BUMPER_PRESSED"/>\n                </block_items>\n                <block_items class="Case" CascadeLabel="REAR_LEFT_BUMPER_PRESSED or REAR_RIGHT_BUMPER_PRESSED">\n                  <expr class="ID" name="REAR_RIGHT_BUMPER_PRESSED"/>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="ID" name="nextState"/>\n                    <rvalue class="ID" name="Driving"/>\n                  </stmts>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="ID" name="makeTransition"/>\n                    <rvalue class="ID" name="TRUE"/>\n                  </stmts>\n                  <stmts class="Assignment" op="=">\n                    <lvalue class="StructRef" type=".">\n                      <name class="ID" name="ThisEvent"/>\n                      <field class="ID" name="EventType"/>\n                    </lvalue>\n                    <rvalue class="ID" name="ES_NO_EVENT"/>\n                  </stmts>\n                  <stmts class="Break"/>\n                </block_items>\n\n-->',
    's00550_add_EventLabel.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<!--\n\n  Handle assignments to nextState guarded by if statements \n\n-->\n<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n  <xsl:template match="*[@NextStateLabel]">\n\n    <xsl:variable name="EventType">\n      <!-- locate first (any) enclosing context\n      that tests EventType (such as some if statement) -->\n      <xsl:for-each\n        select="\n                ancestor::*[@EventTypeTest][1]\n      ">\n        <!-- inside the first enclosing context that tests EventType take the value it is tested\n        against -->\n        \n        <xsl:choose>\n            <xsl:when test="@CascadeLabel">\n                <xsl:value-of select="@CascadeLabel" />\n            </xsl:when>\n            <xsl:otherwise>\n                <xsl:value-of select="@EventTypeTest" />\n            </xsl:otherwise>\n        </xsl:choose>\n        \n      </xsl:for-each>\n    </xsl:variable>\n\n    <xsl:variable name="EventParam">\n      <!-- locate first (any) enclosing context \n      (still inside a switch statement case block) \n      that tests EventParam (such as some if statement)\n      \n        ancestor::*[@EventParamTest][1]\n      \n       -->\n      <xsl:for-each\n        select="\n                ancestor::*[@EventParamTest][1]\n      ">\n        <!-- inside the enclosing context that tests EventParam take the name of what it is tested\n        against -->\n        <xsl:value-of\n          select="\n                @EventParamTest\n        " />\n      </xsl:for-each>\n    </xsl:variable>\n\n    <xsl:variable name="EventLabel">\n      <xsl:choose>\n        <xsl:when test=" normalize-space($EventParam)=\'\' ">\n          <xsl:copy-of select="normalize-space($EventType)" />\n        </xsl:when>\n        <xsl:otherwise>\n          <xsl:text>(</xsl:text>\n          <xsl:copy-of select="normalize-space($EventType)" />\n          <xsl:text>)</xsl:text>\n          <xsl:text>(</xsl:text>\n          <xsl:copy-of select="normalize-space($EventParam)" />\n          <xsl:text>)</xsl:text>\n        </xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n\n    <xsl:copy>\n        <xsl:apply-templates select="@*" />\n        <xsl:attribute name="EventLabel">\n            <xsl:copy-of select="$EventLabel"/>\n        </xsl:attribute>\n\n        <xsl:apply-templates select="node()" />\n    </xsl:copy>\n\n  </xsl:template>\n\n  <!-- identity transform - copy all input nodes to output -->\n  <xsl:template match="@*|node()">\n    <xsl:copy>\n      <xsl:apply-templates select="@*|node()" />\n    </xsl:copy>\n  </xsl:template>\n\n</xsl:stylesheet>',
    's00560_add_Guard_Element.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n    <xsl:key name="line-key" match="/root/code/line" use="@n" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n\n    <xsl:template match="\n        *[\n            @class=\'If\'\n            and not(\n                    (cond[@class=\'BinaryOp\']/left[name/@name=\'ThisEvent\' and field/@name=\'EventType\'] )\n                    or (cond[@class=\'BinaryOp\']/left[name/@name=\'ThisEvent\' and field/@name=\'EventParam\'] )\n                )\n            and (\n                    iftrue/block_items[@NextStateLabel]\n                    or iffalse/block_items[@NextStateLabel]\n            ) \n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n                \n            <xsl:variable name="bLine" select="cond/@bLine"/>\n            <xsl:variable name="eLine" select="cond/@eLine"/>\n\n            <xsl:element name="guard">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine to $eLine">\n                    <xsl:variable name="n" select="string(.)" />\n                    <xsl:for-each select="$currentNode">\n                        <!-- <xsl:copy-of select="/root/code/line[@n = $n]"/> -->\n                        <xsl:copy-of select="key(\'line-key\', $n)" />\n                    </xsl:for-each>        \n                </xsl:for-each>\n            </xsl:element>\n            \n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n\n',
    's00570_add_Guard_Attributes.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <xsl:template match="\n        *[\n            @class=\'If\'\n            and guard\n        ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:attribute name=\'CurrentStateTest\'>\n                <xsl:value-of select="guard/line[1]/@n"/>\n            </xsl:attribute>\n            <xsl:attribute name=\'NextStateLabel\'>\n                <xsl:value-of select="guard/line[1]/@n"/>\n            </xsl:attribute>\n            <xsl:attribute name=\'EventLabel\'>\n                <xsl:choose>\n                    <xsl:when test="..[name()=\'iftrue\']/..[guard]">\n                        <xsl:text>TRUE</xsl:text>\n                    </xsl:when>\n                    <xsl:when test="..[name()=\'iffalse\']/..[guard]">\n                        <xsl:text>FALSE</xsl:text>\n                    </xsl:when>\n                    <xsl:otherwise>\n                        <xsl:value-of select="(.//@EventLabel)[1]"/>\n                    </xsl:otherwise>\n                </xsl:choose>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <xsl:template match="\n        *[\n            @NextStateLabel\n            and not(guard)\n        ]\n    ">\n        <xsl:copy>\n            <xsl:apply-templates select="@*[not(name()=\'EventLabel\')]"/>\n            <xsl:attribute name=\'EventLabel\'>\n                <xsl:choose>\n                    <xsl:when test="..[name()=\'iftrue\']/..[guard]">\n                        <xsl:text>TRUE</xsl:text>\n                    </xsl:when>\n                    <xsl:when test="..[name()=\'iffalse\']/..[guard]">\n                        <xsl:text>FALSE</xsl:text>\n                    </xsl:when>\n                    <xsl:otherwise>\n                        <xsl:value-of select="@EventLabel"/>\n                    </xsl:otherwise>\n                </xsl:choose>\n            </xsl:attribute>\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n</xsl:stylesheet>\n\n',
    's00600_add_onEntry_onExit.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    >\n\n    <!-- xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common" -->\n    \n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n    \n    <xsl:key name="line-key" match="/root/code/line" use="@n" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n    \n    <xsl:template match="*[@CurrentStateTest and not(guard)]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n        \n            <xsl:variable name="bLine1" select=".//*[@EventTypeTest=\'ES_ENTRY\']/@bLine"/>\n            <xsl:variable name="eLine1" select=".//*[@EventTypeTest=\'ES_ENTRY\']/@eLine"/>\n\n            <xsl:element name="onEntry">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine1 to $eLine1">\n                    <xsl:variable name="n" select="string(.)" />\n                    <xsl:for-each select="$currentNode[not($n = $bLine1) and not($n = $eLine1)]">\n                        <!-- <xsl:copy-of select="/root/code/line[@n = $n]"/> -->\n                        <xsl:copy-of select="key(\'line-key\', $n)" />\n                    </xsl:for-each>        \n                </xsl:for-each>\n            </xsl:element>\n        \n            <xsl:variable name="bLine2" select=".//*[@EventTypeTest=\'ES_EXIT\']/@bLine"/>\n            <xsl:variable name="eLine2" select=".//*[@EventTypeTest=\'ES_EXIT\']/@eLine"/>    \n\n            <xsl:element name="onExit">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine2 to $eLine2">\n                    <xsl:variable name="n" select="string(.)" />\n                    <xsl:for-each select="$currentNode[not($n = $bLine2) and not($n = $eLine2)]">\n                        <!-- <xsl:copy-of select="/root/code/line[@n = $n]"/> -->\n                        <xsl:copy-of select="key(\'line-key\', $n)" />\n                    </xsl:for-each>        \n                </xsl:for-each>\n            </xsl:element>\n\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template> \n\n</xsl:stylesheet>\n ',
    's00600_add_onTransition2.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n    xmlns:set="http://exslt.org/sets"\n    xmlns:str="http://exslt.org/strings"\n    xmlns:common="http://exslt.org/common">\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    <xsl:strip-space elements="*" />\n\n    <xsl:key name="line-key" match="/root/code/line" use="@n" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <xsl:template match="*[\n        @NextStateLabel\n        and not(guard)\n        and not(../..[guard])\n    ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n\n            <xsl:variable name="nextStateContext" select="ancestor::*[@EventTypeTest or @EventParamTest][1]"/>\n            <xsl:variable name="bLine" select="$nextStateContext/@bLine"/>\n            <xsl:variable name="eLine" select="$nextStateContext/@eLine"/>\n\n            <xsl:element name="onTransition">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine to $eLine">\n                    <xsl:variable name="n" select="string(.)" />\n                        <xsl:for-each select="$currentNode[not($n = $bLine) and not($n = $eLine)]">\n                            <xsl:copy-of select="key(\'line-key\', $n)" />\n                        </xsl:for-each>\n                </xsl:for-each>\n            </xsl:element>\n\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template> \n\n    <xsl:template match="*[\n        @NextStateLabel \n        and not(guard)\n        and ../..[guard] \n    ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:variable name="guardStateContext" select=".."/>\n            <xsl:variable name="bLine" select="$guardStateContext/@bLine"/>\n            <xsl:variable name="eLine" select="$guardStateContext/@eLine"/>\n            \n            <xsl:element name="onTransition">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine to $eLine">\n                    <xsl:variable name="n" select="string(.)" />\n                        <xsl:for-each select="$currentNode[not($n = $bLine)]">\n                            <xsl:copy-of select="key(\'line-key\', $n)" />\n                        </xsl:for-each>\n                </xsl:for-each>\n            </xsl:element>\n\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n    <xsl:template match="*[\n        @NextStateLabel \n        and guard\n    ]">\n        <xsl:copy>\n            <xsl:apply-templates select="@*"/>\n            <xsl:variable name="guardStateContext" select=".."/>\n            <xsl:variable name="bLine" select="$guardStateContext/@bLine"/>\n            <xsl:variable name="eLine" select="./@bLine"/>\n\n            <xsl:element name="onTransition">\n                <xsl:variable name="currentNode" select="." />\n                <xsl:for-each select="$bLine to $eLine">\n                    <xsl:variable name="n" select="string(.)" />\n                        <xsl:for-each select="$currentNode[not($n = $bLine) and not($n = $eLine)]">\n                            <xsl:copy-of select="key(\'line-key\', $n)" />\n                        </xsl:for-each>\n                </xsl:for-each>\n            </xsl:element>\n\n            <xsl:apply-templates select="node()"/>\n        </xsl:copy>\n    </xsl:template>\n\n\n</xsl:stylesheet>\n ',
    's00620_drop_unwanted_code.xml': '<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n\n    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />\n    <!--   \n    <xsl:output method="html" encoding="UTF-8" />\n     -->\n    \n    <xsl:strip-space elements="*" />\n\n    <xsl:template match="@*|node()">\n        <xsl:copy>\n            <xsl:apply-templates select="@*|node()"/>\n        </xsl:copy>\n    </xsl:template>\n  \n    <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'nextState *=\') ]" />\n    <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'makeTransition *=\') ]" />\n    <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'ThisEvent.EventType *=\') ]" />\n\n    <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'ES_Timer_InitTimer\') ]" />\n    <!-- <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'if *\\(\') ]" /> -->\n    <!-- <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'\\{\') ]" /> -->\n    <!-- <xsl:template match="line[name(..) = \'onTransition\' and matches(.,\'\\}\') ]" /> -->\n\n</xsl:stylesheet>\n',
    's00800_gv_digraph4.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<xsl:stylesheet version="2.0"\n    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n    <xsl:output method="text" />\n\n    <!-- fallback InitState for override -->\n    <xsl:param name="InitState" />\n    <xsl:variable name="ResolvedInitState">\n        <xsl:choose>\n            <xsl:when test="string-length($InitState) > 0">\n                <xsl:value-of select="$InitState" />\n            </xsl:when>\n            <xsl:otherwise>\n                <xsl:value-of select="//ext[@class=\'Decl\' and @name=\'CurrentState\']/init/@name" />\n            </xsl:otherwise>\n        </xsl:choose>\n    </xsl:variable>\n\n    <xsl:template match="/">\n        <xsl:text>\ndigraph fsm {\n\n    // header\n    // rankdir=LR;\n</xsl:text>\n        <xsl:value-of select="$ResolvedInitState" />\n        <xsl:text>[shape = "point", color = "black",style="filled",width=.1,forcelabels=false];\n\n    // states\n    node [shape=plaintext]\n</xsl:text>\n        <!-- original state node rendering logic -->\n        <xsl:for-each\n            select="//*[\n            @CurrentStateTest\n            and not(@CurrentStateTest = \'\')\n            and not(@CurrentStateTest = $ResolvedInitState)\n            and not(guard)\n        ]">\n            <xsl:text>\n    </xsl:text>\n            <xsl:value-of select="@CurrentStateTest" />\n<xsl:text><![CDATA[ [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" style="rounded">\n        <TR>\n            <TD BORDER="1" SIDES="B">]]></xsl:text>\n            <xsl:value-of\n                select="@CurrentStateTest" />\n<xsl:text><![CDATA[</TD>\n        </TR>]]></xsl:text>\n        <xsl:if\n                test="stmts[@class=\'Assignment\' and rvalue/args/exprs/@name=\'ThisEvent\']/lvalue[@name=\'ThisEvent\']">\n                <xsl:text><![CDATA[\n        <TR>\n            <TD ALIGN="LEFT">▶️ ]]></xsl:text>\n            <xsl:value-of\n                    select="stmts[@class=\'Assignment\']/rvalue/name/@name" />\n<xsl:text><![CDATA[</TD>\n        </TR>\n]]></xsl:text>\n            </xsl:if>\n<xsl:text><![CDATA[\n        <TR>\n            <TD ALIGN="LEFT"><B>/Entry: </B></TD>\n        </TR>]]></xsl:text>\n        <xsl:for-each\n                select="onEntry/line">\n                <xsl:text><![CDATA[\n        <TR><TD ALIGN="LEFT">]]></xsl:text>\n            <xsl:value-of select="." />\n<xsl:text><![CDATA[</TD></TR>]]></xsl:text>\n            </xsl:for-each>\n<xsl:text><![CDATA[\n        <TR>\n            <TD ALIGN="LEFT"><B>/Exit: </B></TD>\n        </TR>\n]]></xsl:text>\n        <xsl:for-each\n                select="onExit/line">\n                <xsl:text><![CDATA[<TR><TD ALIGN="LEFT">]]></xsl:text>\n            <xsl:value-of select="." />\n<xsl:text><![CDATA[</TD></TR>\n]]></xsl:text>\n            </xsl:for-each>\n<xsl:text><![CDATA[</TABLE>>];\n\n]]></xsl:text>\n        </xsl:for-each>\n\n        <xsl:text>\n    // guards\n</xsl:text>\n        <xsl:for-each\n            select="//*[@CurrentStateTest and not(@CurrentStateTest = \'\') and not(@CurrentStateTest = \'InitPSubState\') and guard]">\n            <xsl:text>\n    </xsl:text>\n            <xsl:value-of select="@CurrentStateTest" />\n<xsl:text><![CDATA[ [shape=point, xlabel="]]></xsl:text>\n            <xsl:for-each\n                select="guard/line">\n                <xsl:value-of select="." />\n<xsl:text>\n</xsl:text>\n            </xsl:for-each>\n<xsl:text><![CDATA["];\n]]></xsl:text>\n        </xsl:for-each>\n\n        <xsl:text>\n    // transitions\n</xsl:text>\n        <xsl:for-each\n            select="//*[@NextStateLabel]">\n            <xsl:value-of select="ancestor::*[@CurrentStateTest][1]/@CurrentStateTest" />\n            <xsl:text> -> </xsl:text>\n            <xsl:value-of\n                select="@NextStateLabel" />\n<xsl:text><![CDATA[[label=<<TABLE BORDER="0" CELLBORDER="0">\n        <TR><TD BORDER="1" SIDES="B">]]></xsl:text>\n            <xsl:value-of select="@EventLabel" />\n<xsl:text><![CDATA[</TD></TR>]]></xsl:text>\n            <xsl:for-each\n                select="onTransition/line">\n                <xsl:text><![CDATA[\n            <TR><TD ALIGN="LEFT">]]></xsl:text>\n                <xsl:value-of select="." />\n<xsl:text><![CDATA[</TD></TR>]]></xsl:text>\n            </xsl:for-each>\n<xsl:text><![CDATA[\n        </TABLE>>];\n\n]]></xsl:text>\n        </xsl:for-each>\n\n        <xsl:text>\n}\n</xsl:text>\n    </xsl:template>\n</xsl:stylesheet>',
}


@dataclass
class ProjectConfig:
    project_dir: Path
    name: str
    source_roots: list[Path]
    include_dirs: list[Path]
    source_files: list[Path]
    macros: list[str]
    dependency_roots: dict[str, Path]


@dataclass
class GeneratedArtifact:
    source_file: Path
    gv_file: Path
    png_file: Path | None
    cp5_file: Path | None = None
    xml_file: Path | None = None


class VisualizerError(RuntimeError):
    pass


def dedupe_paths(paths: Iterable[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        resolved = str(path.resolve(strict=False)).lower()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def read_text(path: Path) -> str:
    return path.read_text(encoding=ENCODING, errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=ENCODING)


def remove_cache_dir() -> None:
    shutil.rmtree(CACHE_DIR, ignore_errors=True)


def coord_to_line(coord: object) -> str:
    if coord is None:
        return "None"
    match = re.search(r":(\d+)(?::\d+)?$", str(coord))
    return match.group(1) if match else "None"


def prettify_xml(xml_bytes: bytes) -> str:
    return minidom.parseString(xml_bytes).toprettyxml(indent="  ")


def find_projects(root: Path) -> list[Path]:
    projects = []
    if (root / "nbproject" / "configurations.xml").exists():
        return [root]
    for path in root.rglob("*.X"):
        if (path / "nbproject" / "configurations.xml").exists():
            projects.append(path)
    return sorted(projects)


def choose_project_with_gui(initial_dir: Path | None = None) -> Path:
    import tkinter as tk
    from tkinter import filedialog, messagebox

    start_dir = str(initial_dir or Path.home())
    root = tk.Tk()
    root.withdraw()
    selected = filedialog.askdirectory(
        title="Select an MPLAB-X project folder or a parent folder to scan",
        initialdir=start_dir,
    )
    root.destroy()
    if not selected:
        raise VisualizerError("No project folder was selected.")

    picked = Path(selected).resolve(strict=False)
    projects = find_projects(picked)
    if not projects:
        raise VisualizerError(f"No MPLAB-X projects were found under: {picked}")
    if len(projects) == 1:
        return projects[0]

    chooser = tk.Tk()
    chooser.title("Choose MPLAB-X Project")
    chooser.geometry("850x420")

    label = tk.Label(
        chooser,
        text="Multiple MPLAB-X projects were found. Choose the one to visualize:",
        anchor="w",
        justify="left",
    )
    label.pack(fill="x", padx=12, pady=(12, 6))

    frame = tk.Frame(chooser)
    frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, activestyle="dotbox")
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    for project in projects:
        listbox.insert("end", str(project))
    listbox.selection_set(0)

    choice: dict[str, Path | None] = {"path": None}

    def confirm() -> None:
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showerror("No Selection", "Choose a project first.")
            return
        choice["path"] = projects[selected_indices[0]]
        chooser.destroy()

    listbox.bind("<Double-Button-1>", lambda _event: confirm())
    button = tk.Button(chooser, text="Use Selected Project", command=confirm)
    button.pack(pady=(0, 12))
    chooser.mainloop()

    if choice["path"] is None:
        raise VisualizerError("Project selection was cancelled.")
    return choice["path"].resolve(strict=False)


def first_existing_path(candidates: Iterable[Path | None]) -> Path | None:
    for candidate in candidates:
        if candidate is None:
            continue
        candidate = Path(candidate).expanduser().resolve(strict=False)
        if candidate.exists():
            return candidate
    return None


def find_repo_root() -> Path | None:
    for candidate in [ROOT_DIR, *ROOT_DIR.parents]:
        if (candidate / ".git").exists() and (candidate / "Code").exists():
            return candidate
    return None


def current_os() -> str:
    return platform.system().lower()


def framework_root_candidates() -> list[Path]:
    repo_root = find_repo_root()
    os_name = current_os()
    candidates: list[Path] = []
    if repo_root:
        candidates.append(repo_root / "Code")
    if os_name == "windows":
        candidates.append(Path("C:/ECE118"))
    elif os_name == "darwin":
        candidates.extend([
            Path("/ECE118"),
            Path.home() / "ECE118",
            Path.home() / "Documents" / "ECE118",
        ])
    else:
        candidates.extend([
            Path("/ECE118"),
            Path.home() / "ECE118",
            Path.home() / "Documents" / "ECE118",
            Path("/opt/ECE118"),
        ])
    return candidates


def discover_framework_root() -> Path | None:
    env_path = os.getenv(FRAMEWORK_ROOT_ENV)
    return first_existing_path([
        Path(env_path) if env_path else None,
        *framework_root_candidates(),
    ])


def pic32_search_roots() -> list[Path]:
    os_name = current_os()
    if os_name == "windows":
        return [
            Path("C:/Program Files/Microchip/xc32"),
            Path("C:/Program Files (x86)/Microchip/xc32"),
            Path.home() / "Microchip" / "xc32",
        ]
    if os_name == "darwin":
        return [
            Path("/Applications/Microchip/xc32"),
            Path("/opt/microchip/xc32"),
            Path("/usr/local/microchip/xc32"),
            Path.home() / "Microchip" / "xc32",
        ]
    return [
        Path("/opt/microchip/xc32"),
        Path("/usr/local/microchip/xc32"),
        Path.home() / "Microchip" / "xc32",
        Path.home() / ".local" / "microchip" / "xc32",
    ]


def discover_pic32_include() -> Path | None:
    env_path = os.getenv(PIC32_INCLUDE_ENV)
    if env_path:
        path = Path(env_path).expanduser().resolve(strict=False)
        if path.exists():
            return path

    candidates: list[Path] = []
    for root in pic32_search_roots():
        if not root.exists():
            continue
        candidates.extend(root.glob("*/*/include"))
        candidates.extend(root.glob("*/pic32mx/include"))
        candidates.extend(root.glob("**/pic32mx/include"))
    return first_existing_path(candidates)


def collect_nested_dirs(root: Path) -> list[Path]:
    directories = [root]
    for path in root.rglob("*"):
        if path.is_dir():
            directories.append(path)
    return directories


def framework_include_dirs(framework_root: Path | None) -> list[Path]:
    if framework_root is None or not framework_root.exists():
        return []

    include_dirs: list[Path] = [framework_root]
    for child_name in ("include", "src", "templates", "Templates", "Libraries"):
        child = framework_root / child_name
        if child.exists() and child.is_dir():
            include_dirs.extend(collect_nested_dirs(child))
    return dedupe_paths(include_dirs)


def ensure_fake_standard_headers() -> Path:
    fake_root = CACHE_DIR / "fake_headers"
    headers = {
        "stdint.h": """#ifndef _STDINT_H
#define _STDINT_H
typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef short int int16_t;
typedef unsigned short int uint16_t;
typedef int int32_t;
typedef unsigned int uint32_t;
typedef long long int int64_t;
typedef unsigned long long int uint64_t;
typedef int intptr_t;
typedef unsigned int uintptr_t;
#endif
""",
        "inttypes.h": """#ifndef _INTTYPES_H
#define _INTTYPES_H
#include <stdint.h>
#endif
""",
        "stddef.h": """#ifndef _STDDEF_H
#define _STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
typedef int wchar_t;
#define NULL ((void*)0)
#endif
""",
        "stdbool.h": """#ifndef _STDBOOL_H
#define _STDBOOL_H
#define bool _Bool
#define true 1
#define false 0
#endif
""",
        "stdarg.h": """#ifndef _STDARG_H
#define _STDARG_H
typedef int __builtin_va_list;
typedef __builtin_va_list va_list;
#define va_start(ap, last)
#define va_end(ap)
#define va_arg(ap, type) ((type)0)
#endif
""",
        "stdio.h": """#ifndef _STDIO_H
#define _STDIO_H
#include <stddef.h>
typedef struct _SMV_FILE FILE;
int printf(const char *format, ...);
int sprintf(char *buffer, const char *format, ...);
int snprintf(char *buffer, size_t count, const char *format, ...);
#endif
""",
        "stdlib.h": """#ifndef _STDLIB_H
#define _STDLIB_H
#include <stddef.h>
void exit(int status);
void *malloc(size_t size);
void free(void *ptr);
#endif
""",
        "string.h": """#ifndef _STRING_H
#define _STRING_H
#include <stddef.h>
void *memcpy(void *dest, const void *src, size_t n);
void *memset(void *dest, int c, size_t n);
size_t strlen(const char *s);
#endif
""",
        "errno.h": """#ifndef _ERRNO_H
#define _ERRNO_H
typedef int errno_t;
extern int errno;
#endif
""",
        "xc.h": """#ifndef _XC_H
#define _XC_H
#endif
""",
        "sys/attribs.h": """#ifndef _SYS_ATTRIBS_H
#define _SYS_ATTRIBS_H
#define __ISR(vector,ipl)
#define __ISR_AT_VECTOR(vector,ipl)
#endif
""",
    }
    for relative_path, content in headers.items():
        header_path = fake_root / relative_path
        write_text(header_path, content)
    return fake_root


def resolve_external_path(raw_path: str, project_dir: Path, dependency_roots: dict[str, Path]) -> Path:
    candidate = Path(raw_path.replace("/", os.sep))
    if candidate.is_absolute() and candidate.exists():
        return candidate

    relative_candidate = (project_dir / candidate).resolve(strict=False)
    if relative_candidate.exists():
        return relative_candidate

    normalized = raw_path.replace("\\", "/")
    for marker, dependency_root in dependency_roots.items():
        marker_norm = marker.replace("\\", "/")
        if marker_norm.lower() in normalized.lower():
            suffix = normalized.split(marker_norm, 1)[1].lstrip("/")
            mapped = dependency_root / Path(suffix.replace("/", os.sep))
            if mapped.exists():
                return mapped

    if not candidate.is_absolute():
        return relative_candidate
    return candidate


def parse_project_config(project_dir: Path) -> ProjectConfig:
    config_path = project_dir / "nbproject" / "configurations.xml"
    if not config_path.exists():
        raise VisualizerError(f"Could not find MPLAB configuration file: {config_path}")

    framework_root = discover_framework_root()
    pic32_include = discover_pic32_include()
    dependency_roots: dict[str, Path] = {}
    if framework_root is not None and (framework_root / "include").exists() and (framework_root / "src").exists():
        dependency_roots["C:/ECE118"] = framework_root
        dependency_roots["C:\\ECE118"] = framework_root
    if pic32_include is not None:
        dependency_roots["pic32mx"] = pic32_include.parent

    tree = XmlTree.parse(config_path)
    root = tree.getroot()

    source_roots: list[Path] = []
    for node in root.findall(".//sourceRootList/Elem"):
        if node.text:
            source_roots.append(resolve_external_path(node.text.strip(), project_dir, dependency_roots))

    include_dirs: list[Path] = [project_dir, *framework_include_dirs(framework_root)]
    source_files: list[Path] = []
    macros: list[str] = []

    for item in root.findall(".//itemPath"):
        if not item.text:
            continue
        resolved = resolve_external_path(item.text.strip(), project_dir, dependency_roots)
        if resolved.suffix.lower() in SOURCE_SUFFIXES and resolved.exists():
            source_files.append(resolved)
            include_dirs.append(resolved.parent)
        elif resolved.exists() and resolved.is_dir():
            include_dirs.append(resolved)

    for prop in root.findall(".//property[@key='extra-include-directories']"):
        value = prop.attrib.get("value", "")
        for segment in value.split(";"):
            segment = segment.strip()
            if not segment:
                continue
            include_dirs.append(resolve_external_path(segment, project_dir, dependency_roots))

    for prop in root.findall(".//property[@key='preprocessor-macros']"):
        value = prop.attrib.get("value", "")
        for macro in value.split(";"):
            macro = macro.strip()
            if macro:
                macros.append(macro)

    if pic32_include is not None:
        include_dirs.append(pic32_include)

    existing_source_roots = [path for path in source_roots if path.exists()]
    for root_dir in existing_source_roots:
        if root_dir.is_dir():
            include_dirs.append(root_dir)

    include_dirs = [path for path in dedupe_paths(include_dirs) if path.exists()]
    source_files = [path for path in dedupe_paths(source_files) if path.exists()]
    source_roots = dedupe_paths([project_dir, *existing_source_roots])

    return ProjectConfig(
        project_dir=project_dir,
        name=project_dir.stem,
        source_roots=source_roots,
        include_dirs=include_dirs,
        source_files=source_files,
        macros=sorted(set(macros)),
        dependency_roots=dependency_roots,
    )


def collect_macro_names(project: ProjectConfig) -> list[str]:
    macro_names: set[str] = set()
    scan_roots = list(project.include_dirs) + list(project.source_roots)
    for root in dedupe_paths(scan_roots):
        if not root.exists():
            continue
        if root.is_file():
            files = [root]
        else:
            files = [path for path in root.rglob("*") if path.suffix.lower() in SOURCE_SUFFIXES]
        for file_path in files:
            try:
                text = read_text(file_path)
            except OSError:
                continue
            for line in text.splitlines():
                match = re.match(r"^\s*#define\s+([A-Za-z_]\w+)\b(?:\s*\(|\s+)", line)
                if match and len(match.group(1)) > 1:
                    macro_names.add(match.group(1))
    return sorted(macro_names, key=len, reverse=True)


def encode_macros(source_text: str, macro_names: Iterable[str]) -> str:
    encoded = source_text
    for macro_name in macro_names:
        replacement = f"{macro_name[0]}{SENTINEL}{macro_name[1:]}"
        encoded = re.sub(rf"\b{re.escape(macro_name)}\b", replacement, encoded)
    return encoded


class PermissivePreprocessor(Preprocessor):
    def on_include_not_found(self, is_malformed: bool, is_system_include: bool, curdir: str, includepath: str):
        raise OutputDirective(Action.IgnoreAndPassThrough)


def preprocess_with_pcpp(source_file: Path, encoded_source: str, project: ProjectConfig) -> str:
    preprocessor = PermissivePreprocessor()
    for include_dir in project.include_dirs:
        preprocessor.add_path(str(include_dir))

    for macro in project.macros:
        preprocessor.define(macro)

    for define in [
        "RUNNING_VISUALIZER 1",
        "__attribute__(x)",
        "__extension__",
        "__inline__ inline",
        "__restrict__",
        "__PTRDIFF_TYPE__ int",
        "__SIZE_TYPE__ unsigned int",
        "__WCHAR_TYPE__ int",
        "__builtin_va_list int",
    ]:
        preprocessor.define(define)

    preprocessor.parse(encoded_source, str(source_file))
    output = io.StringIO()
    preprocessor.write(output)
    return output.getvalue()


def find_gcc() -> str | None:
    for candidate in ("gcc", "gcc.exe"):
        located = shutil.which(candidate)
        if located:
            return located
    return None


def preprocess_with_gcc(source_file: Path, encoded_source: str, project: ProjectConfig, gcc_path: str) -> str:
    scratch_dir = CACHE_DIR / "preprocessed_sources"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    fake_header_root = ensure_fake_standard_headers()
    temp_source = scratch_dir / f"{source_file.name}.undef"
    write_text(temp_source, encoded_source)
    command = [
        gcc_path,
        "-E",
        "-P",
        "-x",
        "c",
        "-nostdinc",
        "-DRUNNING_VISUALIZER",
        f"-I{fake_header_root}",
        *[f"-D{macro}" for macro in project.macros],
        *[f"-I{include_dir}" for include_dir in project.include_dirs],
        str(temp_source),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    temp_source.unlink(missing_ok=True)
    if result.returncode != 0:
        raise VisualizerError(
            f"Preprocessor failed for {source_file}.\n"
            f"Command: {' '.join(command)}\n{result.stderr.strip()}"
        )
    return result.stdout


def clean_preprocessed_source(source_text: str) -> str:
    cleaned = source_text.replace(SENTINEL, "")
    substitutions = [
        (r"\b__extension__\b", " "),
        (r"\s+__attribute__\s*\(\(.*\)\)\);", ";"),
        (r"\s+__attribute__\s*\(\(.*\)\)\)", ""),
        (r"\b__attribute__\s*\(\(.*?\)\)", " "),
        (r"\b__inline__\b", " "),
        (r"\b__restrict__\b", " "),
        (r"\b__signed\b", "signed"),
        (r"\b__volatile__\b", "volatile"),
        (r"\b__const\b", "const"),
        (r"\basm\s*\([^;]*\);", ";"),
        (r"\b__asm__\s+volatile\s*\([^;]*\);", ";"),
        (r"\b__builtin_unreachable\s*\(\s*\);", ";"),
    ]
    for pattern, replacement in substitutions:
        cleaned = re.sub(pattern, replacement, cleaned)
    cleaned = re.sub(r"\r\n?", "\n", cleaned)
    lines = []
    for line in cleaned.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if "va_list" in line or "__attribute__" in line:
            continue
        lines.append(line)
    return "\n".join(lines)


def preprocess_source(source_file: Path, project: ProjectConfig, macro_names: list[str]) -> str:
    encoded_source = encode_macros(read_text(source_file), macro_names)
    gcc_path = find_gcc()
    if gcc_path:
        return clean_preprocessed_source(preprocess_with_gcc(source_file, encoded_source, project, gcc_path))
    return clean_preprocessed_source(preprocess_with_pcpp(source_file, encoded_source, project))


def build_xml_ast(preprocessed_source: str, source_file: Path) -> tuple[str, CParser]:
    parser = CParser()
    ast = parser.parse(preprocessed_source, str(source_file))

    def add_node(node, xnode: ET._Element) -> ET._Element:
        xnode.set("class", node.__class__.__name__)
        xnode.set("line", coord_to_line(node.coord))
        for attribute_name in node.attr_names:
            value = getattr(node, attribute_name)
            xnode.set(attribute_name, "" if value is None else str(value))
        for child_name, child in node.children():
            normalized_name = re.sub(r"\[.*\]", "", child_name)
            child_node = ET.SubElement(xnode, normalized_name)
            add_node(child, child_node)
        return xnode

    root = ET.Element("root")
    code_node = ET.SubElement(root, "code")
    for index, line in enumerate(preprocessed_source.splitlines(), start=1):
        line_node = ET.SubElement(code_node, "line")
        line_node.text = line
        line_node.set("n", str(index))
    root.append(add_node(ast, ET.Element("ast")))
    return prettify_xml(ET.tostring(root)), parser


class XsltPipeline:
    def __init__(self) -> None:
        self.processor = PySaxonProcessor(license=False)
        self.xslt_processor = self.processor.new_xslt30_processor()
        self.chain = [
            self.xslt_processor.compile_stylesheet(stylesheet_text=XSLT_ASSETS[xslt_name])
            for xslt_name in XSLT_CHAIN
        ]
        self.final = self.xslt_processor.compile_stylesheet(stylesheet_text=XSLT_ASSETS[FINAL_XSLT])

    def render_graphviz(self, xml_text: str, init_state: str) -> str:
        current_node = self.processor.parse_xml(xml_text=xml_text)
        for executable in self.chain:
            transformed = executable.transform_to_string(xdm_node=current_node)
            current_node = self.processor.parse_xml(xml_text=transformed)
        self.final.clear_parameters()
        self.final.set_parameter("InitState", self.processor.make_string_value(init_state))
        return self.final.transform_to_string(xdm_node=current_node)

    def close(self) -> None:
        self.processor = None
        self.xslt_processor = None
        self.chain = []
        self.final = None


def detect_init_state(preprocessed_source: str) -> str:
    match = re.search(r"\bCurrentState\s*=\s*([A-Za-z_]\w*)", preprocessed_source)
    return match.group(1) if match else "InitPSubState"


def find_dot(dot_override: str | None = None) -> str | None:
    candidates: list[Path | str] = []
    if dot_override:
        candidates.append(dot_override)
    env_dot = os.getenv(GRAPHVIZ_DOT_ENV)
    if env_dot:
        candidates.append(env_dot)
    os_name = current_os()
    if os_name == "windows":
        candidates.extend(
            [
                "dot",
                "dot.exe",
                Path("C:/Program Files/Graphviz/bin/dot.exe"),
                Path("C:/Program Files (x86)/Graphviz/bin/dot.exe"),
            ]
        )
    elif os_name == "darwin":
        candidates.extend(["dot", Path("/opt/homebrew/bin/dot"), Path("/usr/local/bin/dot")])
    else:
        candidates.extend(["dot", Path("/usr/bin/dot"), Path("/usr/local/bin/dot")])
    for candidate in candidates:
        resolved = shutil.which(str(candidate)) or (str(candidate) if Path(candidate).exists() else None)
        if resolved:
            return resolved
    return None


def find_gvedit() -> str | None:
    candidates: list[Path | str] = []
    env_gvedit = os.getenv(GVEDIT_ENV)
    if env_gvedit:
        candidates.append(env_gvedit)
    os_name = current_os()
    if os_name == "windows":
        candidates.extend(
            [
                "gvedit",
                "gvedit.exe",
                Path("C:/Program Files/Graphviz/bin/gvedit.exe"),
                Path("C:/Program Files (x86)/Graphviz/bin/gvedit.exe"),
            ]
        )
    elif os_name == "darwin":
        candidates.extend(["gvedit", Path("/opt/homebrew/bin/gvedit"), Path("/usr/local/bin/gvedit")])
    else:
        candidates.extend(["gvedit", Path("/usr/bin/gvedit"), Path("/usr/local/bin/gvedit")])
    for candidate in candidates:
        resolved = shutil.which(str(candidate)) or (str(candidate) if Path(candidate).exists() else None)
        if resolved:
            return resolved
    return None


def make_output_prefix(output_root: Path, source_file: Path, source_roots: list[Path]) -> Path:
    for root in source_roots:
        try:
            relative = source_file.resolve(strict=False).relative_to(root.resolve(strict=False))
            return output_root / relative
        except ValueError:
            continue
    return output_root / source_file.name


def discover_state_machine_sources(project: ProjectConfig, source_filter: str | None = None) -> list[Path]:
    candidates = []
    for source_file in project.source_files:
        if source_file.suffix.lower() != ".c":
            continue
        if source_filter and source_filter.lower() not in source_file.name.lower():
            continue
        try:
            text = read_text(source_file)
        except OSError:
            continue
        if "nextState" in text:
            candidates.append(source_file)
    return dedupe_paths(candidates)


def run_dot(dot_path: str, gv_file: Path, png_file: Path) -> None:
    command = [dot_path, "-Tpng", str(gv_file), "-o", str(png_file)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise VisualizerError(f"Graphviz failed for {gv_file}:\n{result.stderr.strip()}")


def launch_gvedit(gv_file: Path) -> None:
    gvedit = find_gvedit()
    if gvedit:
        subprocess.Popen([gvedit, str(gv_file)])
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(str(gv_file))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(gv_file)])
        else:
            subprocess.Popen(["xdg-open", str(gv_file)])
    except OSError:
        pass


def generate_diagrams(
    project: ProjectConfig,
    output_root: Path,
    dot_path: str | None,
    open_viewer: bool,
    source_filter: str | None = None,
    keep_intermediate: bool = False,
) -> list[GeneratedArtifact]:
    macro_names = collect_macro_names(project)
    sources = discover_state_machine_sources(project, source_filter)
    if not sources:
        raise VisualizerError(f"No C files containing 'nextState' were found for project {project.name}.")

    artifacts: list[GeneratedArtifact] = []
    pipeline = XsltPipeline()
    try:
        for source_file in sources:
            print(f"[smv] Visualizing {source_file}", flush=True)
            preprocessed = preprocess_source(source_file, project, macro_names)
            xml_text, _ = build_xml_ast(preprocessed, source_file)
            init_state = detect_init_state(preprocessed)
            gv_text = pipeline.render_graphviz(xml_text, init_state)

            prefix = make_output_prefix(output_root, source_file, project.source_roots)
            cp5_file = prefix.with_suffix(prefix.suffix + ".cp5")
            xml_file = prefix.with_suffix(prefix.suffix + ".xml")
            gv_file = prefix.with_suffix(prefix.suffix + ".gv")
            png_file = prefix.with_suffix(prefix.suffix + ".png") if dot_path else None

            if keep_intermediate:
                write_text(cp5_file, preprocessed)
                write_text(xml_file, xml_text)
            write_text(gv_file, gv_text)

            if dot_path and png_file is not None:
                run_dot(dot_path, gv_file, png_file)

            artifacts.append(
                GeneratedArtifact(
                    source_file=source_file,
                    gv_file=gv_file,
                    png_file=png_file,
                    cp5_file=cp5_file if keep_intermediate else None,
                    xml_file=xml_file if keep_intermediate else None,
                )
            )

            if open_viewer:
                launch_gvedit(gv_file)
    finally:
        pipeline.close()

    return artifacts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize MPLAB-X state machines as Graphviz diagrams.")
    parser.add_argument(
        "--project",
        help="Path to an MPLAB-X project folder (.X) or a parent folder to scan.",
    )
    parser.add_argument(
        "--output",
        help="Directory for generated files. Defaults to the project directory.",
    )
    parser.add_argument(
        "--dot",
        help="Path to Graphviz dot executable. If omitted, the script searches common locations.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open each generated .gv file in GVedit or the OS default app after generation.",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Fail instead of opening a folder picker when --project is omitted.",
    )
    parser.add_argument(
        "--source-filter",
        help="Only process source files whose filename contains this text.",
    )
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Also keep the intermediate .cp5 and .xml files for debugging.",
    )
    return parser.parse_args()


def resolve_project_path(cli_project: str | None, no_gui: bool) -> Path:
    if cli_project:
        chosen = Path(cli_project).expanduser().resolve(strict=False)
        projects = find_projects(chosen)
        if not projects:
            raise VisualizerError(f"No MPLAB-X projects were found under: {chosen}")
        if len(projects) == 1:
            return projects[0].resolve(strict=False)
        if no_gui:
            raise VisualizerError(
                "Multiple MPLAB-X projects were found. Re-run with a specific .X directory or allow the GUI picker."
            )
        return choose_project_with_gui(chosen)

    if no_gui:
        raise VisualizerError("No project path was provided and --no-gui was requested.")
    return choose_project_with_gui()


def main() -> int:
    args = parse_args()
    try:
        project_path = resolve_project_path(args.project, args.no_gui)
        project = parse_project_config(project_path)
        output_root = (
            Path(args.output).expanduser().resolve(strict=False)
            if args.output
            else project.project_dir.resolve(strict=False)
        )
        output_root.mkdir(parents=True, exist_ok=True)

        dot_path = find_dot(args.dot)
        if dot_path is None:
            print("[smv] Graphviz 'dot' was not found. .gv files will still be generated, but .png files will be skipped.")

        artifacts = generate_diagrams(
            project,
            output_root,
            dot_path,
            args.open,
            args.source_filter,
            args.keep_intermediate,
        )

        print()
        print(f"[smv] Project: {project.project_dir}")
        print(f"[smv] Output : {output_root}")
        print(f"[smv] Files  : {len(artifacts)} state machine source file(s) processed")
        for artifact in artifacts:
            png_text = str(artifact.png_file) if artifact.png_file else "not generated"
            print(f"[smv]   {artifact.source_file.name} -> {artifact.gv_file} | png: {png_text}")
        return 0
    except VisualizerError as error:
        print(f"[smv] ERROR: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # pragma: no cover
        print(f"[smv] Unexpected error: {error}", file=sys.stderr)
        return 1
    finally:
        remove_cache_dir()


if __name__ == "__main__":
    raise SystemExit(main())

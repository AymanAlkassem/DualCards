# DualCards
# Auto-generated DualCards cloze add-on

from aqt import mw, gui_hooks

NOTE_TYPE_NAME = "DualCards"

FRONT_TEMPLATE = """<div id="hidden" style="visibility:hidden; height:0; overflow:hidden; position:absolute;">
  <span id="t1">{{cloze:Field1}}</span>
  <span id="t2">{{cloze:Field2}}</span>
</div>

<div id="fraga" style="font-size:20px; text-align:center; visibility:hidden;"></div>

<script>
  var text1 = document.getElementById("t1").innerHTML.trim();
  var text2 = document.getElementById("t2").innerHTML.trim();
  document.getElementById("hidden").remove();

  // Dela upp strängen så Anki inte tolkar den som cloze-syntax
  var clozeMarkering = "{" + "{c";

  function arGiltig(text) {
    return text !== "" && !text.includes(clozeMarkering);
  }

  var harText1 = arGiltig(text1);
  var harText2 = arGiltig(text2);

  var val = 0;

  if (harText1 && harText2 && document.body.classList.contains("card")) {
    val = Math.random() < 0.5 ? 0 : 1;
  } else if (!harText1 && harText2) {
    val = 1;
  }

  window._valtFalt = val;

  var fraga = document.getElementById("fraga");
  fraga.innerHTML = val === 0 ? text1 : text2;
  fraga.style.visibility = "visible";
</script>"""

BACK_TEMPLATE = """<div id="hidden" style="display:none">
  <span id="t1">{{cloze:Field1}}</span>
  <span id="t2">{{cloze:Field2}}</span>
</div>

<div id="fraga" style="font-size:20px; text-align:center;"></div>

<div style="font-size:20px; text-align:center; color:gray;">
  {{Extra}}
</div>

<script>
  var text1 = document.getElementById("t1").innerHTML.trim();
  var text2 = document.getElementById("t2").innerHTML.trim();
  document.getElementById("hidden").remove();

  var val = window._valtFalt !== undefined ? window._valtFalt : Math.floor(Math.random() * 2);

  var fraga = document.getElementById("fraga");
  fraga.innerHTML = val === 0 ? text1 : text2;
</script>

"""

CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}

.hint {
    font-size: 7px;
    color: gray !important;
}

.hint[style*="display: inline;"] {
    color: black !important;
}

#body {
	margin: 0;
	border-top: solid 1px #3b9500
;
	padding-top: 10px;
}"""

FIELDS = ["Field1", "Field2", "Extra"]


def create_note_type():
    col = mw.col
    existing = col.models.by_name(NOTE_TYPE_NAME)
    if existing:
        return

    m = col.models.new(NOTE_TYPE_NAME)
    m["type"] = 1  # cloze type

    for field_name in FIELDS:
        fld = col.models.new_field(field_name)
        col.models.add_field(m, fld)

    t = col.models.new_template("DualCards Card")
    t["qfmt"] = FRONT_TEMPLATE
    t["afmt"] = BACK_TEMPLATE
    col.models.add_template(m, t)

    m["css"] = CSS
    col.models.add(m)
    col.models.save(m)


def on_profile_loaded():
    create_note_type()


gui_hooks.profile_did_open.append(on_profile_loaded)

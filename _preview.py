import base64, pathlib
ROOT = pathlib.Path(__file__).parent
FACES = [("Superglue","Superglue.otf","opentype"),("Courbe Sans","CourbeSans.ttf","truetype"),
         ("Violent Brave","ViolentBrave.ttf","truetype"),("Comangs","Comangs.ttf","truetype"),
         ("Messy Melted","MessyMelted.ttf","truetype"),("Cyasren","Cyasren.otf","opentype"),
         ("Ophium","Ophium.ttf","truetype")]
b64 = {}
ff = ""
for fam, fn, fmt in FACES:
    data = base64.b64encode((ROOT/"fonts"/fn).read_bytes()).decode()
    b64[fam] = data
    ext = "otf" if fmt == "opentype" else "ttf"
    ff += f"@font-face{{font-family:'{fam}';src:url(data:font/{ext};base64,{data}) format('{fmt}');font-display:block}}\n"
ff += ("@font-face{font-family:'Courbe Sans';font-display:block;"
       f"src:url(data:font/ttf;base64,{b64['Comangs']}) format('truetype');"
       "unicode-range:U+2013,U+2014,U+2022,U+00B7;}\n")
base = (ROOT/"assets"/"base.css").read_text()
out = pathlib.Path("/home/claude/preview"); out.mkdir(exist_ok=True)
for k in ["001","002","003","004"]:
    body = (ROOT/"zines"/f"{k}.html").read_text()
    (out/f"{k}.html").write_text(
        f"<!DOCTYPE html><html><head><meta charset='UTF-8'><style>{ff}</style><style>{base}</style></head><body>{body}</body></html>")
print("previews written")

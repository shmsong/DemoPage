r"""
    Generate Static HTML required to post on github
"""

from os import listdir
import argparse

front_matter = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Automaticaly generated content, please update scripts/htmlgen.py for any change -->
   <head>
      <meta charset="UTF-8">
      <title align="center">blah blah"</title>
      <style type="text/css">
        body, input, select, td, li, div, textarea, p {
        	font-size: 11px;
        	line-height: 16px;
        	font-family: verdana, arial, sans-serif;
        }

        body {
        	margin:5px;
        	background-color:white;
        }

        h1 {
        	font-size:16px;
        	font-weight:bold;
        }

        h2 {
        	font-size:14px;
        	font-weight:bold;
        }
      </style>
   </head>
   <body>
      <article>
         <header>
            <h1>aaa</h1>
         </header>
      </article>

      <div>
      Website license info sheet <a href = https://yolanda-gao.github.io/Interactive-Style-TTS/Interactive_TTS_license.pdf >pdf</a>
      </div>


      <div>
        <h2>Abstract</h2>
        <p> While modern TTS technologies have made significant advancements in audio quality, there is still a lack of behavior naturalness compared to conversing with people. We propose a style-embedded TTS system that generates styled responses based on the speech query style. To achieve this, the system includes a style extraction model that extracts a style embedding from the speech query, which is then used by the TTS to produce a matching response. We faced two main challenges: 1) only a small portion of the TTS training dataset has style labels, which is needed to train a multi-style TTS that respects different style embeddings during inference. 2) The TTS system and the style extraction model have disjoint training datasets. We need consistent style labels across these two datasets so that the TTS can learn to respect the labels produced by the style extraction model during inference. To solve these, we adopted a semi-supervised approach that uses the style extraction model to create style labels for the TTS dataset and applied transfer learning to learn the style embedding jointly. Our experiment results show user preference for the styled TTS responses and demonstrate the style-embedded TTS system’s capability of mimicking the speech query style.</p>
      </div>

      <h2> Contents </h2>
      <div id="toc_container">
         <ul>
            <b> <a href="#Style">A: Style TTS samples</a> </b><br/>
            <b> <a href="#RenderingLevel">B: Controllable styles </a> </b><br/>
            <b> <a href="#Matching">C: Real-life input queries and responses</a> </b><br/>
         </ul>
      </div>
"""

back_matter = r"""
   </body>
</html>
"""
def get_row_column():
    Columns = listdir('./Asset')
    assert len(Columns) >0, 'No subfolders under Asset/'
    Rows = listdir(f"./Asset/{Columns[0]}")
    for c in Columns:
        assert set(listdir(f"./Asset/{c}")) == set(Rows)
    return Rows,Columns

def gen_table_header(cols=["nothing"],file=None):
    print(r"""
    <div>
    <h2> Samples </h2>
      <table border = "1" class="inlineTable">
    """,file=file)
    print(
    ''.join([r"""
        <col width="300">""" for  _ in cols]),
        file=file)
    print(
    """     <tr> """,file=file)
    print(
    ''.join([f"""
        <th>{col}</th>""" for  col in cols])+
    """ 
    </tr>"""
    ,file=file)

def audio_entry(audio,file=None):
    print(
    f"""
    <td>
        <audio controls style="width: 200px;">
        <source src={audio} type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </td>""",file=file)

def text_entry(text,file=None):
    print(
        f"""
        <th>{text}</th>""",
        file=file)

def single_row(columns,text=True,file=None):
    print("<tr>",file=file)
    for c in columns:
        if(text):
            text_entry(c,file=file)
        else:
            audio_entry(c,file=file)
    print("</tr>",file=file)
    
    

def gen_table(args,file=None):
    rows,cols = get_row_column()
    gen_table_header(cols,file=file)
    for r in rows:
        c = [f"./Asset/{x}/{r}" for x in cols]
        single_row(c,text=args.name_only,file=file)
    print("""
        </table>
    </div>
    """,file=file)

def main(args):
    fname = args.output
    with open(fname,'w') as f:
        print(front_matter,file=f)
        gen_table(args,file=f)
        print(back_matter,file=f)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o','--output', type=str, default='index.html',help='output name')
    parser.add_argument('-n','--name_only', action="store_true",help='put file names only')
    args = parser.parse_args()

    main(args)
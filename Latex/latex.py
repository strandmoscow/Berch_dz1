import numpy as np
from jinja2 import Environment, FileSystemLoader
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def matr_to_table(mat):
    s = ""
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            s = s + f"{str(mat[i][j])}"
            if j < len(mat[0])-1:
                s = s + " & "
        if i < len(mat)-1:
            s = s + " \\\\\n"
    return s


def tabl_to_table(mat, n):
    s = ""
    for i in range(len(mat) - 1):
        s = s + f"{i+1} & {mat[i][1] / n} & {mat[i][2] / n} & {mat[i][3] / n} & {mat[i][4] / n} & {mat[i][5] / n} \\\\\n \\hline "
    s = s + f"{len(mat)} & {mat[len(mat) - 1][1] / n} & {mat[len(mat) - 1][2] / n} & {mat[len(mat) - 1][3] / n} & {mat[len(mat) - 1][4] / n} & {mat[len(mat) - 1][5] / n} \\\\\n \\hline"
    return s


def ispr_ocen(matr):
    a1 = np.empty(len(matr))
    a2 = np.empty(len(matr))
    a3 = np.empty(len(matr))
    a4 = np.empty(len(matr))
    a5 = np.empty(len(matr))
    for i in range(len(matr)):
        a1[i] = matr[i][1] / 100.
        a2[i] = matr[i][2] / 100.
        a3[i] = matr[i][3] / 100.
        a4[i] = matr[i][4] / 100.
        a5[i] = matr[i][5] / 100.

    return f"{'%.3f' % np.sqrt(20 * np.var(a1)/(20 - 1))} & {'%.3f' % np.sqrt(20 * np.var(a2)/(20 - 1))} & {'%.3f' % np.sqrt(20 * np.var(a3)/(20 - 1))} & {'%.3f' % np.sqrt(20 * np.var(a4) / (20 - 1))} & {'%.3f' % np.sqrt(20 * np.var(a5) / (20 - 1))}"


def make_latex(var_num, group, fullname, fullname_short, stohast_matr, vect_pred_ver, sates_matr):
    # Jinja init
    environment = Environment(
        loader=FileSystemLoader("Latex/templates/")
    )

    # Preambule text
    base_template = environment.get_template("educmm_lab_Variant_N_M-id.tex")
    base_res_file_name = "Latex/res/labs/educmm_txb_COMPMATHLAB-Solution_N_M/educmm_lab_Variant_N_M-id.tex"
    base_text = base_template.render(
        author_name=fullname,
        author_name_short=fullname_short,
        group=group,
        variant=var_num
    )
    with open(base_res_file_name, mode="w+", encoding="utf-8") as base:
        base.write(base_text)
        print(f"... wrote {base_res_file_name}")

    # Main text
    latex_text_template = environment.get_template("educmm_txb_COMPMATHLAB-Solution_N_M.tex")
    latex_text_file_name = f"Latex/res/labs/educmm_txb_COMPMATHLAB-Solution_N_M.tex"
    latex_text = latex_text_template.render(
        stohast_matr=matr_to_table(stohast_matr),
        vect_pred_ver=vect_pred_ver,
        tabl_otn_chast_nabl=tabl_to_table(sates_matr, 100),
        ispr_oc=ispr_ocen(sates_matr)
    )
    with open(latex_text_file_name, mode="w+", encoding="utf-8") as text:
        text.write(latex_text)
        print(f"... wrote {latex_text_file_name}")

    # Graph text
    graph_template = environment.get_template("graph.svg")
    graph_file_name_svg = f"Latex/res/Images/graph.svg"
    graph_file_name_png = f"Latex/res/Images/graph.png"
    graph_text = graph_template.render(
        stohast_matr=stohast_matr
    )
    with open(graph_file_name_svg, mode="w+", encoding="utf-8") as text:
        text.write(graph_text)
        print(f"... wrote {graph_file_name_svg}")
    drawing = svg2rlg(graph_file_name_svg)
    renderPM.drawToFile(drawing, graph_file_name_png, fmt='PNG')




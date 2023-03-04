from jinja2 import Environment, FileSystemLoader


def make_latex(var_num, group, fullname, fullname_short, stohast_matr, vect_pred_ver, sates_matr):

    # Jinja init
    environment = Environment(
        loader=FileSystemLoader("Latex/templates/")
    )

    base_template = environment.get_template("educmm_lab_Variant_N_M-id.tex")

    base_res_file_name = "Latex/res/labs/educmm_txb_COMPMATHLAB-Solution_N_M/educmm_lab_Variant_N_M-id.tex"

    base_text = base_template.render(
        author_name=fullname,
        author_name_short=fullname_short,
        group=group,
        variant=var_num
    )

    print(base_text)

    with open(base_res_file_name, mode="w+", encoding="utf-8") as base:
        base.write(base_text)
        print(f"... wrote {base_res_file_name}")




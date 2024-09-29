


def untangle_job_data(job_data):
    untangled_data = []
    for job in job_data:
        untangled_data.append({
            'company': job['company'],
            'job_description': job['job_description'].split('\n'),
            'job_title': job['job_title'],
            'project': job['project'],
            'location': job['location']
        })
    return untangled_data

def convert_to_latex(resume_points):
    
    latex_string = ""
    for point in resume_points["experiences"]:
        latex_string += "\\WorkExperience\n"
        latex_string += "{" + point['company'] + "}\n"
        latex_string += "{" + point['job_title'] + "}\n"
        latex_string += "{\n"
        latex_string += "\\vpsace{-1pt}\n"
        # latex_string += "{" + point['location'] + "}\n"
        # latex_string += "{\n"
        for desc in point['job_description']:
            latex_string += "    \\item " + desc + "\n"
        latex_string += "}\n"
        latex_string += "\\vspace{2pt}\n"

    # replace the last \vspace{2pt} with \vspace{-7pt}
    latex_string = latex_string[:-13] + "\\vspace{-7pt}\n"
    return latex_string

def write_to_latex_file(latex_string, company_name):
    # Replace the place holder {WORK_EXPERIENCE} with the latex_string and save it to a new file
    with open('data/template.tex', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('{WORK_EXPERIENCE}', latex_string)

    with open(f'data/My_Resume_{company_name}.tex', 'w') as file:
        file.write(filedata)

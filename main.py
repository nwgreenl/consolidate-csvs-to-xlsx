import datetime, os, re, sys, pandas as pd
from tkinter import filedialog

# cwd
cwd = os.getcwd()

# get files via tkinter filedialog
def get_files():
    files = filedialog.askopenfilenames(initialdir=cwd, title="Select File", filetypes=[("CSV Files", ".csv")])
    
    if len(files) == 0:
        sys.exit("\nNo Files Selected... Goodbye!\n")
    
    return list(files)

# output dir (assumes it's in root folder)
def get_outputdir(dirName="output"):
    output_dir = "%s/%s" % (cwd, dirName)
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    return output_dir

# output file 
def get_outputfile(fileName="consolidated", dirName="output", append_date=True):
    output_ext = "xlsx"
    output_dir = get_outputdir(dirName)
    output_date = datetime.datetime.now().strftime("%m-%d-%Y_%I-%M") 

    if append_date:
        output_filename = "%s_%s" % (fileName, output_date)
    else:
        output_filename = "%s_%s" % fileName

    output_file = "%s/%s.%s" % (output_dir, output_filename, output_ext)
    
    return output_file

# progress bar, thanks @eusoubrasileiro
def progressbar(it, prefix="Running: ", size=50, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

# consolidate
def consolidate_files(files, output_file):  
    # sheet name regex
    illegal_chars = re.compile("[^a-zA-Z0-9]")

    try:        
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            for i in progressbar(range(len(files))): 
                for file in files:
                    # sheet names must be <= 31 chars and cannot contain "\ / * ? : ,"
                    # opting to remove any char that isn't a word or digit
                    filename_for_sheet = illegal_chars.sub("", os.path.basename(file)).replace("csv", "")[:31]
                    
                    df = pd.read_csv(file)
                    df.to_excel(writer, sheet_name=filename_for_sheet, header=False, index=False)

        # success message
        is_input_plural = "s" if len(files) > 1 else ""

        print("\nSuccessfully created '%s' using the following CSV%s:" % (os.path.basename(output_file), is_input_plural))
        for file in files:
            print("  - %s" % os.path.basename(file))    

    except Exception as e:
        print("Error encountered while consolidating files")
        print(e)

# do the things
consolidate_files(get_files(), get_outputfile())
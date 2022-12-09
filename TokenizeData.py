
import os
import subprocess
import shutil
import glob

def _run_tokenizer(folder_path, out_folder, tokenizer_path, tokenizer_language, tokenizer_level,count):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    file_counter = 1
    out_file = os.path.join(out_folder, "tokenized" + str(count)+str(file_counter) + ".tok")
    for file in os.listdir(folder_path):
        input_file = os.path.abspath(os.path.join(folder_path, file))
        try:
            print("\t\tprocessing " + file)
        except:
            pass
        in_file = os.path.abspath(os.path.join(out_folder, "temp.tok"))
        if os.path.exists(in_file):
            os.remove(in_file)
        with open(in_file, "w+", errors='ignore') as tok_out_file:
            exe_path = os.path.abspath(tokenizer_path)
            x=subprocess.run([exe_path, "-l", tokenizer_language, "-o",
                              tokenizer_level, input_file], stdout=tok_out_file)

        with open(out_file, "a", errors='ignore') as f:
            with open(in_file, "r", errors='ignore') as in_f:
                tok_text = in_f.read()
            f.write(tok_text.lstrip("b'").rstrip("'\\n"))
        os.remove(in_file)
        if os.path.getsize(out_file) > 52428800: #50 mb
            file_counter += 1
            out_file = os.path.join(out_folder, "tokenized" +  str(count)+str(file_counter) + ".tok")


def tokenize(tokenizer_language, tokenizer_input_base_path, tokenizer_out_base_path, tokenizer_exe_path,count):
    if not os.path.exists(tokenizer_out_base_path):
        os.makedirs(tokenizer_out_base_path)

    list = ["UnutilizedAbstraction","LongStatement","MagicNumber"]
    assert tokenizer_language == "Java"

    for dir in list:
        tokenizer_level = "file"
        cur_base_folder = os.path.join(tokenizer_input_base_path, dir)

        print("\t processing positive cases...")
        cur_folder = os.path.join(cur_base_folder, "Positive")
        out_folder = os.path.join(os.path.join(os.path.join(tokenizer_out_base_path,
                                                            dir)), "Positive")
        _run_tokenizer(cur_folder, out_folder, tokenizer_exe_path, tokenizer_language, tokenizer_level,count)

        print("\t processing negative training cases...")
        cur_folder = os.path.join(cur_base_folder, "Negative")
        out_folder = os.path.join(os.path.join(os.path.join(tokenizer_out_base_path,
                                                            dir)), "Negative")
        _run_tokenizer(cur_folder, out_folder, tokenizer_exe_path, tokenizer_language, tokenizer_level,count)
    print("Tokenizing done.")
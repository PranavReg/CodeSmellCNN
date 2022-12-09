import os
import git
import glob
import time
import codeSmellDetectDesignate
import CodeSplit
import Labledata
import TokenizeData

if __name__ == "__main__":
    RepoListfile=r'G:\ProjectList.txt'
    JAVA_SMELLS_RESULTS_FOLDER=r"G:\zzz\DesignateResults"
    DESIGNITE_JAVA_JAR_PATH="C:\\Users\\ranad\\Downloads\\DesigniteJava.jar"
    JAVA_CODE_SPLIT_OUT_FOLDER_CLASS = r'G:\zzz\codesplit_java_class'
    JAVA_CODE_SPLIT_OUT_FOLDER_METHOD = r'G:\zzz\codesplit_java_method'
    JAVA_CODE_SPLIT_MODE_CLASS = "class"
    JAVA_CODE_SPLIT_MODE_METHOD = "method"
    JAVA_CODE_SPLIT_EXE_PATH = r'C:\Users\ranad\Desktop\Pranav\Studies\Data Analytics in Software Engineering\Project\CodeSplitJava.jar'
    JAVA_LEARNING_DATA_FOLDER_BASE = r'G:\zzz\learningDataOutput'
    Tokenizer_Out_Path = r'G:\zzz\TokenDataOutPut'
    Tokenizer_Exe_Path = r'G:\tokenizer-master\src\tokenizer.exe'

    repo_list =[]
    with open(RepoListfile) as f:
        for line in f:
            repo_list.append(line.strip())
    for i in repo_list:
      c=i.split("/")
      projectName=c[0]+"-"+c[1]
      REMOTE_REPO_URL="https://github.com/"+i
      JAVA_REPO_SOURCE_FOLDER="G:\\CloneRepo\\"+projectName
      try:
          git.Repo.clone_from(REMOTE_REPO_URL, JAVA_REPO_SOURCE_FOLDER)
      except git.GitCommandError as e:
          if("smudge filter lfs failed" in e.stderr):
              print("Git LFS Error, Not downloading the LFS files")
              pass
          elif("Repository not found" in e.stderr): #Ignoring the project if the repo is not found in github
              print("Repository not found in GitHUb,",i)
              continue


      codeSmellDetectDesignate.analyze_repositories(JAVA_REPO_SOURCE_FOLDER, JAVA_SMELLS_RESULTS_FOLDER+"\\"+projectName, DESIGNITE_JAVA_JAR_PATH)

      CodeSplit.java_code_split(JAVA_REPO_SOURCE_FOLDER, JAVA_CODE_SPLIT_MODE_CLASS,JAVA_CODE_SPLIT_OUT_FOLDER_CLASS+"\\"+projectName, JAVA_CODE_SPLIT_EXE_PATH)
      CodeSplit.java_code_split(JAVA_REPO_SOURCE_FOLDER, JAVA_CODE_SPLIT_MODE_METHOD,JAVA_CODE_SPLIT_OUT_FOLDER_METHOD+"\\"+projectName, JAVA_CODE_SPLIT_EXE_PATH)
      time.sleep(5)

      Labledata.generate_data(JAVA_SMELLS_RESULTS_FOLDER+"\\"+projectName, JAVA_CODE_SPLIT_OUT_FOLDER_CLASS+"\\"+projectName,JAVA_CODE_SPLIT_OUT_FOLDER_METHOD+"\\"+projectName, JAVA_LEARNING_DATA_FOLDER_BASE+"\\"+projectName)

    count=0
    for filename in glob.iglob(f'{JAVA_LEARNING_DATA_FOLDER_BASE}\*'):
        count+=1
        TokenizeData.tokenize("Java",filename,Tokenizer_Out_Path,Tokenizer_Exe_Path,count)


import texFileWriter, graphsFileWriter

#input1 = input("Enter input path and out path separated by comma:\n").split(", ")
in_path = "D:\\Dropbox\\MB_various\\UNL\\Data\\tex_study_34"  # input1[0]
out_path = "D:\\Dropbox\\MB_various\\UNL\\Data" + "\\report"  # input1[1] + "\\report"
texFileWriter.write_file(in_path, out_path)
graphsFileWriter.write_file(in_path, out_path)

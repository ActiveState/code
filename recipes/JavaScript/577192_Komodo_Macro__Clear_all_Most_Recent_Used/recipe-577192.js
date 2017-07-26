var arrMRU = [
"compare_files_first",
"compare_files_second",
"find-foldersMru",
"find-patternMru",
"find_findInFilesFieldMru",
"mruFileList",
"mruProjectList",
"mruTemplateList",
"new-dirnameMru",
"new-filenameMru",
"run-commandMru",
"run-commandStringMru",
"run-cwdMru",
"run-parseRegexMru"];

for (m in arrMRU) {
    var mru = ko.mru.getAll(arrMRU[m]);
    ko.mru.reset(arrMRU[m]);
}

version 1.0

workflow md5Sum {
input {
File inputFile
}

call calculateMd5Sum {
input:
inputFile = inputFile
}

output {
String md5 = calculateMd5Sum.md5
}
}

task calculateMd5Sum {
input {
File inputFile
String outname = basename(inputFile) + ".md5"
}

command <<<
gsutil hash -m ~{inputFile} | grep -E 'Hash \(md5\):\s' | cut -f4 > ~{outname}
>>>

output {
String md5 = read_string("${outname}")
}

runtime {
docker: "google/cloud-sdk:slim"
cpu: 1
memory: "3.75 GB"
disks: "local-disk 10GB HDD"
}
}

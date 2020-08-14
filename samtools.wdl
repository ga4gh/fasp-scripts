version 1.0
task samtools_stats {
  input {
    File bam
  }
  String output_name = bam + ".stats"
  command <<<
    samtools stats ~{bam} > ~{output_name}
  >>>
  output {
    File stats = "~{output_name}"
  }
  runtime {
    docker: "gcr.io/genomics-tools/samtools"
    cpu: 1
    memory: "3.75 GB"
  }
}
workflow run_samtools_stats {
  input {
    File bam
  }
  call samtools_stats {
    input:
      bam = bam,
  }
  output {
    File stats = samtools_stats.stats
  }
}
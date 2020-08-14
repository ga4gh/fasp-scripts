version 1.0
task samtools_stats {
  input {
    File bam
    File bam_index
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
    File bam_index
  }
  call samtools_stats {
    input:
      bam = bam,
      bam_index = bam_index
  }
  output {
    File stats = samtools_stats.stats
  }
}
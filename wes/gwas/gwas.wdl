version 1.0

workflow gwas {
	input {
		File vcf
		File metadata_csv
	}

	call parse_metadata {
		input:
			metadata_csv = metadata_csv
	}

	call run_gwas {
		input:
			vcf = vcf,
			covariates = parse_metadata.covariates,
			phenotypes = parse_metadata.phenotypes,
			sex = parse_metadata.sex,
			ids = parse_metadata.ids
	}

	call create_plot {
		input:
			assoc_file = run_gwas.logistic
	}

	output {
		File logistic = run_gwas.logistic
		File manhattan_plot = create_plot.manhattan_plot
	}
}

task parse_metadata {
	input {
		File metadata_csv
	}

	command <<<
		# generate covariates file using Super_Population column
		echo "FID IID Super_Population" > covariates.txt
		awk -vFPAT='[^,]*|"[^"]*"' 'NR > 1 {print $2,$1,$61}' ~{metadata_csv} >> covariates.txt
		## recode covariates to numerical
		sed -i -e 's/AFR$/1/g' -e 's/AMR$/2/g' -e 's/EAS$/3/g' -e 's/EUR$/4/g' -e 's/SAS$/5/g' covariates.txt

		# generate phenotypes file; assume phenotype is in the last column
		echo "FID IID Simulated_disease" > phenotypes.txt
		awk -vFPAT='[^,]*|"[^"]*"' 'NR > 1 {print $2,$1,$NF}' ~{metadata_csv} >> phenotypes.txt

		# generate sex file
		echo "FID IID Sex" > sex.txt
		awk -vFPAT='[^,]*|"[^"]*"' 'NR > 1 {{if ($5=="female") sex=2; else if ($5=="male") sex=1; else sex=0} {print $2,$1,sex}}' ~{metadata_csv} >> sex.txt

		# generate ID update file
		echo "OLD_FID OLD_IID NEW_FID NEW_IID" > ids.txt
		awk -vFPAT='[^,]*|"[^"]*"' 'NR > 1 {print $1,$1,$2,$1}' ~{metadata_csv} >> ids.txt
	>>>

	output {
		File covariates = "covariates.txt"
		File phenotypes = "phenotypes.txt"
		File sex = "sex.txt"
		File ids = "ids.txt"
	}

	runtime {
		docker: "dnastack/plink:1.9"
		cpu: 1
		memory: "3.75 GB"
		disks: "local-disk 20 HDD"
	}
}

task run_gwas {
	input {
		File vcf
		File covariates
		File phenotypes
		File sex
		File ids
	}

	Int disk_size = ceil(size(vcf, "GB") * 2 + 50)
	String output_basename = basename(vcf, ".vcf.gz")

	command {
		plink \
			--vcf ~{vcf} \
			--maf 0.10 \
			--update-ids ~{ids} \
			--make-bed \
			--out ~{output_basename}

		plink \
			--bfile ~{output_basename} \
			--update-sex ~{sex} \
			--pheno ~{phenotypes} \
			--make-bed \
			--out ~{output_basename}

		# Recode covariates to binary
		plink \
			--bfile ~{output_basename} \
			--covar ~{covariates} \
			--dummy-coding \
			--write-covar

		plink \
			--bfile ~{output_basename} \
			--logistic \
			--covar plink.cov \
			--out ~{output_basename}

		sed -i -e 's/\s\+/,/g' -e 's/^,//g' -e 's/,$//g' ~{output_basename}.assoc.logistic
	}

	output {
		File logistic = "~{output_basename}.assoc.logistic"
	}

	runtime {
		docker: "dnastack/plink:1.9"
		cpu: 4
		memory: "16 GB"
		disks: "local-disk " + disk_size + " HDD"
		preemptible: 2
	}
}

task create_plot {
	input {
		File assoc_file
	}

	String assoc_basename = basename(assoc_file, ".assoc.logistic")

	command {
		manhattan_plot.py \
			-i ~{assoc_file} \
			-o ~{assoc_basename}.png
	}

	output {
		File manhattan_plot = "~{assoc_basename}.png"
	}

	runtime {
		docker: "dnastack/plink:1.9"
		cpu: 2
		memory: "7.5 GB"
		disks: "local-disk 20 HDD"
	}
}



class Aliger:
    def __init__(self, args):
        self.args=args


    def run_blastp(self, file_ref):
        blast_db=os.path.splitext(file_ref)[0]
        outfile=os.path.splitext(self.args.file_faa)[0]+'.blast'
        if not os.path.isfile(blast_db+'.nhr'):
            print('\n\n###Build a new blast database\n')
            command="makeblastdb -dbtype prot -in {} -out {}".format(file_ref, blast_db)
            self.run_tool(command)
        #
        print('\n\n###Run proein-protein blast:\n')
        exe='blastp -evalue 1e-10 -num_threads 24 -outfmt 6 -num_alignments 5'
        command="{} -query {} -db {} -out {}".format(exe, \
                      self.args.file_faa, blast_db, outfile)
        self.run_tool(command)        

    def run_blastn(self):
        if not os.path.isfile(self.args.blast_db+'.nhr'):
            print('\n\n###Build a new blast database\n')
            command="makeblastdb -dbtype nucl -in {} -out {}".format(\
                       self.args.file_fa, self.args.blast_db)
            self.run_tool(command)
        #
        print('\n\n###Run DNA-DNA blast:\n')
        exe='tblastn -evalue 0.001 -num_threads 24 -outfmt 7'
        blast_query='/mnt/rdedata12/yuan/AltriaSeq/bacteria_odb9/ancestral'
        command="{} -query {} -db {} -out {}".format(exe, blast_query,\
                          self.args.blast_db, self.args.blast_out)
        self.run_tool(command) 
        
        
    def run_blat(self, reads):
        fasta_file = self.args.dir_results + '/R2C2_temp_for_BLAT.fasta'
        input_file_fasta = open(fasta_file, 'w')
        for read in reads:
            input_file_fasta.write(">{}\n{}\n".format(read, reads[read][0]))
        input_file_fasta.close()
        #
        outfile=self.args.dir_results+'Splint_to_read_alignments.psl'
        os.system('blat -noHead -stepSize=1 -t=DNA q=DNA -minScore=15 \
              -minIdentity=10 %s %s %s' %(self.args.file_splint, fasta_file, outfile))        

#        
    def run_hisat2(self, sample_name):
        
        #initiate 
        sample_dir=Dir(self.args.dir_results+sample_name+'/').formate_dir()
        sample_prefix=sample_dir+sample_name
        sample_sam_file=sample_prefix+'.sam'
        novel_ss_file=sample_prefix+'_novel_ss.txt'
        summary_file=sample_prefix+'_summary.log'
        met_file=sample_prefix+'_met.log'
        sample_R1_str=self.args.sample_R1[sample_name]
        #print(sample_R1_str)
        
        #
        hisat2_basic="hisat2 -p 4 -q --dta --phred33 -x {} -S \"{}\"".format(\
                self.args.genome_index, sample_sam_file)
        hisat2_options = "{} --novel-splicesite-outfile {}  --summary-file {} --met-file {}".format(\
                          hisat2_basic, novel_ss_file, summary_file, met_file)
        if self.args.single_end is True:
            command = "{} -U \"{}\" ".format(hisat2_options, sample_R1_str)
        else:
            sample_R2_str=self.args.sample_R2[sample_name]
            #print(sample_R2_str)
            command = "{} -1 \"{}\" -2 \"{}\" ".format(hisat2_options,\
                           sample_R1_str, sample_R2_str)

        #print shell_command
        if not os.path.isfile(sample_sam_file):
            print('\n\n#######Sequence alignment', sample_name)
            self.run_tool(command)
 
        return 

    def run_samtools(self, sample_name, sample_dir=None):
        #initiate 
        if sample_dir is None:
            sample_dir=self.args.dir_results+sample_name
        dir_prefix=ab.basic().format_dir(sample_dir)+sample_name
        sample_sam_file=dir_prefix+'.sam'
        sample_bam_file=dir_prefix+'_sorted.bam'

        #convert sam to bam
        command="samtools sort -@ 24 -o \"{}\" \"{}\"; pigz {} ".format(\
                    sample_bam_file, sample_sam_file, sample_sam_file)
        if not os.path.isfile(sample_bam_file):
            print('Convert sam file into bam file: ', sample_name)
            self.run_tool(command)      
       
        #create RC table
        return 
        
    
    def run_stringtie(self, sample_name):
        #initiate 
        self.args.sample_dir=ab.basic().format_dir(self.args.dir_results+sample_name)
        self.args.sample_prefix=self.args.sample_dir+sample_name
        sample_bam_file=self.args.sample_prefix+'_sorted.bam'
        sample_gtf_file=self.args.sample_prefix+'.gtf'
                
        #assemble transcripts
        if not os.path.isfile(sample_gtf_file):
            command="stringtie -G \"{}\" -o \"{}\" -l {} \"{}\" ".format(\
                        self.args.genome_gtf_file, sample_gtf_file, sample_name, sample_bam_file)
            self.run_tool(command)
        
        #create RC table
        return 

#nanopore
#query_file could fastq or fasta
    def run_minimap2_cdna(self,ref_file=None, bam_file=None):
        if ref_file is None:
            ref_file=self.args.genome_fa_file
        index_file=os.path.splitext(ref_file)[0]+'.mmi'
        #12-1:build index if it doesn't exist
        if not os.path.isfile(index_file):
            exe = "minimap2 -t 24 -k 14 -I 1000G"
            command = "{} -d {} {}".format(exe, index_file, ref_file)
            self.run_tool(command)
            
        #12-2:alignment
        if bam_file is None:
            bam_file=self.args.bam_file
        minimap2 = "minimap2 -t 24 -ax splice -uf"
        samtools = "samtools view -q 10 -F 2304 -Sb | samtools sort -@ 24"
        command="{} {} {} | {} -o {}; samtools index {}".format(minimap2,\
            index_file, self.args.query_file, samtools, bam_file, bam_file)
        self.run_tool(command)
        #
        return 1



    def run_mirdeep2(self, sample_name):
        '''
        mirdeep2 for miRNA
        '''
        print('\n\n###Analyze {}: {}\n'.format(sample_name, self.args.sample_R1[sample_name]))
        outdir=ab.basic().format_dir(self.args.dir_results+sample_name)
        file_reads=outdir+'reads_collapsed.fa'
        file_arf=outdir+'reads_vs_refdb.arf'
        #mapper
        exe='mapper.pl {} -e -p {} -k {}'.format(self.args.sample_R1[sample_name], 
                       self.args.genome_index, self.args.adapter_3end)
        command = "cd {}; {} -h -i -j -n -l 18 -m -v -o 24 -s {} -t {}".format(
                        outdir, exe, file_reads, file_arf)
        self.run_tool(command)      
        
        #mirdeep2
        file_mature=self.args.dir_genome+'mirbase_mature_nta.fa'
        file_others=self.args.dir_genome+'mirbase_mature_others.fa'
        file_precursor=self.args.dir_genome+'mirbase_hairpin_nta.fa'
        log=outdir+'report.log'
        command = "cd {}; miRDeep2.pl {} {} {} {} {} {} 2>{}".format(outdir, file_reads, \
            self.args.genome_fa_file, file_arf, file_mature, file_others, file_precursor, log)
        self.run_tool(command) 
#end

class AssemblyTool:
    @staticmethod
    def run_gffcompare(self, dir_results, dir_pinfish, genome_gtf_file):
        '''
        compare gff files
        '''
        #  pinfish/polished_transcripts_collapsed.gff -o gff_compare
        exe="gffcompare -R -M -C -K"
        outdir=ab.basic().format_dir(args.dir_results+'gffcompare')+'gffcompare'
        gff_col = dir_pinfish+'polished_transcripts_collapsed.gff'
        command = "{} -r {} -o {} {}".format(exe, genome_gtf_file, outdir, gff_col)
        #print(command)
        Threading.run_tool(command)

"""

"""
import os
import re


class FASTA:

    @staticmethod
    def read_fa(self, fa_file):
        '''
        read fasta used for karyotype.txt of circos
        '''
        print('elicit dna information from ', fa_file)
        #store accession: sequences
        ref_dict = {'chr':''}
        ref_list = ['chr']
        in_obj=ab.basic().readonly_handle(fa_file)
        #read fa file
        for line in in_obj:
            line = line.rstrip()
            if line.find(">") == 0:
                #fa_id = self.acc_number(line)
                fa_id = re.sub(r"^>", "", line.split(" ")[0])
                ref_list.append(fa_id)
                ref_dict[fa_id] = []
                self.record_num += 1
            else:
                ref_dict[fa_id].append(line)
        in_obj.close()
        
        #arrage ref
        total_len=0
        pos_start=0
        pos_end=-1
        ref_start={}
        ref_end={}
        for fa_id in ref_list[1:]:
            #print fa_id, ref_dict[fa_id][:3], "\n"
            ref_dict[fa_id] = ''.join(ref_dict[fa_id])
            ref_dict['chr'] += ref_dict[fa_id]
            #
            pos_start = pos_end+1
            ref_start[fa_id]=pos_start
            pos_end = total_len + len(ref_dict[fa_id])
            ref_end[fa_id]=pos_end
            #print(ref_start[fa_id], ref_end[fa_id], len(ref_dict[fa_id]))
            
            #update for the next
            total_len += len(ref_dict[fa_id])
            
            #print fa_id, len(re.findall('^N*', ref_dict[fa_id])[0]), len(ref_dict[fa_id]),'\n'
        ref_start['chr']=0
        ref_end['chr']=total_len
        #print(ref_end['chr'])
        return ref_dict, ref_list, ref_start,ref_end
    
    @staticmethod
    def fa_dict(self, file_fa):
        '''
        '''
        n=0
        #store accession: sequences
        ref_dict = {}
        ref_list = []
        in_obj=ab.basic().readonly_handle(file_fa)
        #read fa file
        for line in in_obj:
            line = line.rstrip()
            if line.find(">") == 0:
                #acc = self.acc_number(line)
                acc = re.sub(r"^>", "", line.split(" ")[0])
                ref_list.append(acc)
                ref_dict[acc] = []
                n+=1
            else:
                ref_dict[acc].append(line)
        in_obj.close()
        print('Number of sequences:', n)
        return ref_dict, ref_list
    
    @staticmethod
    def read_fa_files(self, outfile, genome_names, sub_args):
        '''
        outfile is combine them into one fasta file 
        used by mcscanx
        '''
        fa_dict={}
        fa_obj=open(outfile, 'w')
        for name in genome_names:
            sub_args=sub_args[name]
            #read AA
            ref_dict, ref_list=FASTA.fa_dict(sub_args.file_faa)
            #print('\n\n\n%%%', ref_list)
            #export
            for ID in ref_list:
                key=name+'_'+ID
                #if key in aa_gene:
                #    print(aa_gene[key]['genome'], key, name)
                fa_dict[key]={'geneID':ID, 'aa_seq':''.join(ref_dict[ID]), 'gff':None}
                fa_obj.write(">{}\n{}\n".format(key, ''.join(ref_dict[ID])))
        fa_obj.close()
        return fa_dict

        
        

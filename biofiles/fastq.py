from Bio import Seq, SeqIO, SeqRecord

class FASTQ:
    def __init__(self, fq_file):
        self.fq_file = fq_file

    def read_fq(self):
        '''
        Takes a FASTQ file and returns dictionary of lists
        readDict {'name_root':['full_header', seq, quality]...}
        '''
        readDict = {}
        lineNum, lastPlus, lastHead, skip = 0, False, '', False
        for line in open(self.fastq_file):
            line = line.rstrip()
            if not line:
                continue
            if lineNum % 4 == 0 and line[0] == '@':
                name = line[1:].split()[0]
                readDict[name], lastHead = [], name
            if lineNum % 4 == 1:
                readDict[lastHead].append(line)
            if lineNum % 4 == 2:
                lastPlus = True
            if lineNum % 4 == 3 and lastPlus:
                avgQ = sum([ord(x)-33 for x in line])/len(line)
                sLen = len(readDict[lastHead][-1])
                if avgQ >= self.par['quality_cutoff'] and sLen >= self.par['read_length_cutoff']:
                    readDict[lastHead].append(line)
                    readDict[lastHead] = tuple(readDict[lastHead])
                else:
                    del readDict[lastHead]
                lastPlus, lastHead = False, ''
            lineNum += 1
        return readDict

    def write_fq(self, adapter_dict, reads, outdir):
        success = 0
        os.system('mkdir ' + self.par['dir_results']  + '/splint_reads')
        for read in reads:
            name, sequence, quality = read, reads[read][0], reads[read][1]
            adapter_plus = sorted(adapter_dict[name]['+'],key=lambda x: x[1], reverse=True)
            adapter_minus=sorted(adapter_dict[name]['-'], key=lambda x: x[1], reverse=True)
            plus_list_name, plus_list_position = [], []
            minus_list_name, minus_list_position = [], []

            for adapter in adapter_plus:
                if adapter[0] != '-':
                    plus_list_name.append(adapter[0])
                    plus_list_position.append(adapter[2])
            for adapter in adapter_minus:
                if adapter[0] != '-':
                    minus_list_name.append(adapter[0])
                    minus_list_position.append(adapter[2])

            if len(plus_list_name) > 0 or len(minus_list_name) > 0:
                success += 1
                splint_file = outdir + 'splint_reads/' + str(int(success/4000)) + '/R2C2_raw_reads.fastq'
                try:
                    out_fastq = open(splint_file, 'a')
                except:
                    os.system('mkdir ' + self.par['dir_results']  + '/splint_reads/' + str(int(success/4000)))
                    out_fastq = open(splint_file, 'w')
                    list_pos=  str(plus_list_position[0]) if len(plus_list_name) > 0 else str(minus_list_position[0])
                    out_fastq.write('@' + name + '_' + list_pos + '\n' + sequence + '\n+\n' + quality + '\n')
            else:
                no_splint_file = outdir + 'splint_reads/No_splint_reads.fastq'
                try:
                    out_fastq = open(no_splint_file, 'a')
                except:
                    out_fastq = open(no_splint_file, 'w')
                    out_fastq.write('>' + name + '\n' + sequence + '\n+\n' + quality + '\n')

    def demultiplexing(self, indir):
        pass

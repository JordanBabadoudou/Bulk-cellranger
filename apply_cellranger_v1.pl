#use!/usr/bin/perl
use strict;
use warnings;
use File::Basename;

# Paramètres à ajuster
my $base_dir = "/home/jordan23/scratch/def-ytanaka/jordan23/Patient_scRNA-main/text/";
my $transcriptome = "/home/jordan23/scratch/def-ytanaka/jordan23/refgen/refdata-gex-GRCh38-2024-A/";
my $cpu = 2;
my $tmpdir = "/home/jordan23/scratch/def-ytanaka/jordan23/output";

# Obtenir la liste des répertoires
opendir(my $dh, $base_dir) or die "Impossible d'ouvrir le répertoire $base_dir: $!";
my @directories = grep { -d "$base_dir/$_" && ! /^\./ } readdir($dh);
closedir($dh);

my $count = scalar @directories;
my $time = time();

# Vérifier s'il y a des répertoires à traiter
if ($count == 0) {
    die "Aucun répertoire trouvé dans $base_dir\n";
}

# Créer le fichier temporaire
my $tmp = "$tmpdir/" . basename($0) . "_$time";
open(my $OUT, '>', $tmp) or die "Impossible d'ouvrir $tmp : $!";

# Écrire l'en-tête du script Slurm
print $OUT "#!/bin/bash\n";
print $OUT "#SBATCH --time=36:00:00\n";
print $OUT "#SBATCH --account=def-ytanaka\n";
print $OUT "#SBATCH --ntasks=1\n";
print $OUT "#SBATCH --cpus-per-task=$cpu\n";
print $OUT "#SBATCH --mem=180G\n";
print $OUT "#SBATCH --array=0-" . ($count - 1) . "\n";
print $OUT "module load gcc/12.3\n";
print $OUT "module load StdEnv/2023\n";
print $OUT "export PATH=/home/jordan23/scratch/def-ytanaka/jordan23/cellranger-8.0.1/bin:\$PATH\n";

# Écrire les commandes cellranger count
print $OUT "directories=(", join(" ", @directories), ")\n";
print $OUT "dir=\${directories[\$SLURM_ARRAY_TASK_ID]}\n";
print $OUT "cd $base_dir/\$dir\n";
print $OUT "cellranger count --id=\$dir \\\n";
print $OUT "                 --transcriptome=$transcriptome \\\n";
print $OUT "                 --fastqs=. \\\n";
print $OUT "                 --create-bam=true\\\n";
print $OUT "                 --localcores=\$SLURM_CPUS_PER_TASK \\\n";
print $OUT "                 --localmem=70\n";

close $OUT;

# Lancer le job Slurm
system("sbatch $tmp");

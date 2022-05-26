# Configuration file automatically generated at 2022-05-15 for /Users/davidluongo/Documents/Local_Mac_Dev/575/Project/bob1/bin/verify.py.

##################################################
############### REQUIRED ARGUMENTS ###############
##################################################

# These arguments need to be set.


# Database and the protocol; registered databases are: ['asvspoof-licit', 'asvspoof-spoof', 'asvspoof2017-licit', 'asvspoof2017-spoof', 'avspoof-licit', 'avspoof-spoof', 'mobio-audio-female', 'mobio-audio-male', 'timit', 'voicepa-licit', 'voicepa-spoof', 'voxforge']
import bob.bio.base.database
import bob.bio.gmm.algorithm
from bob.bio.spear.database import AudioBioFile
# database = 'voxforge'
database = bob.bio.base.database.FileListBioDatabase('../../databases/toy_database', 'toy',
                                                     original_directory='../../databases/corpora/untarred/ru/wav',
                                                     original_extension='.wav',
                                                     bio_file_class=AudioBioFile)


# Data preprocessing; registered preprocessors are: ['cqcc20p', 'energy-2gauss', 'energy-thr', 'external', 'filename', 'mod-4hz']

preprocessor = 'energy-2gauss'


# Feature extraction; registered feature extractors are: ['cqcc20e', 'htk', 'imfcc20', 'lfcc-60', 'lfcc20', 'linearize', 'mfcc-60', 'mfcc20', 'rfcc20', 'scfc20', 'scmc20', 'spro', 'ssfc20']

extractor = 'mfcc-60'


# Algorithm of the experiment; registered algorithms are: ['bic', 'distance-cosine', 'distance-euclidean', 'distance-hamming', 'gmm-banca', 'gmm-timit', 'gmm-tomi', 'gmm-tomi-scfc', 'gmm-voxforge', 'isv-avspoof', 'isv-mobio', 'isv-voxforge', 'ivec-avspoof', 'ivec-cosine-voxforge', 'ivec-plda-mobio', 'ivec-plda-voxforge', 'jfa-voxforge', 'lda', 'pca', 'pca+lda', 'pca+plda', 'plda']

algorithm = 'isv-voxforge' #bob.bio.gmm.algorithm.GMM(200)


# The sub-directory where the files of the current experiment should be stored. Please specify a directory name with a name describing your experiment

sub_directory = 'output'


##################################################
################ COMMON ARGUMENTS ################
##################################################

# These arguments are commonly changed.


# Configuration for the grid setup; if not specified, the commands are executed sequentially on the local machine; registered grid resources are ['demanding', 'gpu', 'grid', 'local-p16', 'local-p4', 'local-p8', 'modest'].

#grid = None


# The groups (i.e., 'dev', 'eval') for which the models and scores should be generated; by default, only the 'dev' group is evaluated

groups = ['dev', 'eval']


# Overwrite the protocol that is stored in the database by the given one (might not by applicable for all databases).

#protocol = None


# The directory for temporary files; if --temp-directory is not specified, "temp" is used

temp_directory = '../temp'


# The directory for resulting score files; if --result-directory is not specified, "results" is used

result_directory = 'results/test_exp'


# Increase the verbosity level from 0 (only error messages) to 1 (warnings), 2 (log messages), 3 (debug information) by adding the --verbose option as often as desired (e.g. '-vvv' for debug).

verbose = 2


# Only report the commands that will be executed, but do not execute them.

# dry_run = True


# Force to erase former data if already exist

force = True


# Enable the computation of ZT norms

#zt_norm = False


# If given, missing files will not stop the processing; this is helpful if not all files of the database can be processed; missing scores will be NaN.

#allow_missing_files = False


# This flag is a shortcut for running the commands on the local machine with the given amount of parallel processes; equivalent to --grid bob.bio.base.grid.Grid("local", number_of_parallel_processes=X) --run-local-scheduler --stop-on-failure.

#parallel = None


##################################################
############### OPTIONAL ARGUMENTS ###############
##################################################

# Files and directories might commonly be specified with absolute paths or relative to the temp_directory.
# Change these options, e.g., to reuse parts of other experiments.


# Name of the file to write the feature extractor into.

#extractor_file = 'Extractor.hdf5'


# Name of the file to write the feature projector into.

#projector_file = 'Projector.hdf5'


# Name of the file to write the model enroller into.

#enroller_file = 'Enroller.hdf5'


# Name of the directory of the preprocessed data.

#preprocessed_directory = 'preprocessed'


# Name of the directory of the extracted features.

#extracted_directory = 'extracted'


# Name of the directory where the projected data should be stored.

#projected_directory = 'projected'


# Name of the directory where the models (and T-Norm models) should be stored

#model_directories = ['models', 'tmodels']


##################################################
############ RARELY CHANGED ARGUMENTS ############
##################################################


# If one of your configuration files is an actual command, please specify the lists of required libraries (imports) to execute this command

#imports = ['bob.bio.base']


# If resources with identical names are defined in several packages, prefer the one from the given package

#preferred_package = None


# The database file in which the submitted jobs will be written; relative to the current directory (only valid with the --grid option).

#gridtk_database_file = 'submitted.sql3'


# The file where the configuration of all parts of the experiments are written; relative to te --result-directory.

#experiment_info_file = 'Experiment.info'


# An optional file, where database directories are stored (to avoid changing the database configurations)

# database_directories_file = './config/bob_bio_databases.txt'


# Name of the directory (relative to --result-directory) where to write the results to

#score_directories = ['nonorm', 'ztnorm']


# Name of the directories (of --temp-directory) where to write the ZT-norm values; only used with --zt-norm

#zt_directories = ['zt_norm_A', 'zt_norm_B', 'zt_norm_C', 'zt_norm_D', 'zt_norm_D_sameValue']


# Name of the directory (relative to --temp-directory) where to log files are written; only used with --grid

#grid_log_directory = 'gridtk_logs'


# Writes score files in five-column format (including the model id)

#write_five_column_score_files = False


# Writes score files which are compressed with tar.bz2.

#write_compressed_score_files = False


# Try to recursively stop the dependent jobs from the SGE grid queue, when a job failed

#stop_on_failure = False


# The jobs submitted to the grid have dependencies on the given job ids.

#external_dependencies = []


# Measure and report the time required by the execution of the tool chain (only on local machine)

#timer = None


# Starts the local scheduler after submitting the jobs to the local queue (by default, local jobs must be started by hand, e.g., using ./bin/jman --local -vv run-scheduler -x)

#run_local_scheduler = False


# Runs the local scheduler with the given nice value

#nice = 10


# If selected, local scheduler jobs that finished with the given status are deleted from the --gridtk-database-file; otherwise the jobs remain in the database

#delete_jobs_finished_with_status = None


# Performs score calibration after the scores are computed.

#calibrate_scores = False


# Passes specific environment variables to the job.

#env = []


# Skip the preprocessing step.

#skip_preprocessing = False


# Skip the extractor-training step.

#skip_extractor_training = False


# Skip the extraction step.

#skip_extraction = False


# Skip the projector-training step.

#skip_projector_training = False


# Skip the projection step.

#skip_projection = False


# Skip the enroller-training step.

#skip_enroller_training = False


# Skip the enrollment step.

#skip_enrollment = False


# Skip the score-computation step.

#skip_score_computation = False


# Skip the concatenation step.

#skip_concatenation = False


# Skip the calibration step.

#skip_calibration = False


# If specified, executes only the given parts of the tool chain.

#execute_only = None



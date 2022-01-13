#!/bin/bash
helpFunction()
{
   echo ""
   echo "Usage: $0 -n modelName -f modelFolder -v version -o outputDIr"
   echo -e "\t-n Name of model to be created"
   echo -e "\t-f Target folder of model"
   echo -e "\t-v Model version"
   echo -e "\t-o Output directory"
   exit 1 # Exit script after printing help
}

while getopts "n:f:v:o:" opt
do
   case "$opt" in
      n ) modelName="$OPTARG" ;;
      f ) modelFolder="$OPTARG" ;;
      v ) version="$OPTARG" ;;
      o ) outputDir="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$modelName" ] || [ -z "$modelFolder" ] || [ -z "$version" ] || [ -z "$outputDir" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
torch-model-archiver --model-name $modelName \
--version $version \
--serialized-file models/$modelFolder/pytorch_model.bin \
--export-path ./$outputDir -f \
--handler ModelHandler.py \
--extra-files models/$modelFolder/extra_files \
-r requirements.txt

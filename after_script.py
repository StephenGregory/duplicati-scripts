import argparse
import json
import os
import logging
from datetime import timedelta

import arrow
import jsonpickle

from Exporters import Webhook
from Operations import Backup, Operation

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.basicConfig(filename='after_script.log', level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler(r'D:\Application Data\Projects\Software\Python\Duplicati\after_script.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def main(operation_result_details, duplicati_env_vars):
    # type: (dict, dict(str, str)) -> None

    exporters = list()

    exporters.append(Webhook('https://hook.integromat.com/u4h25ndqu36hlao74erjv2x2wsnvlixg'))

    logger.debug('Result:')
    logger.debug(operation_result_details)

    logger.debug('Available env vars:')
    for k, v in duplicati_env_vars.iteritems():
        logger.debug(k)

    # file_hash_algorithm
    # dbpath
    # blocksize
    # localpath
    # backup_name
    # log_level
    # disable_module
    # main_action
    # run_script_result_output_format
    # remoteurl
    # encryption_module
    # dblock_size
    # eventname
    # run_script_after
    # no_encryption
    # compression_module
    # block_hash_algorithm
    # operationname
    # run_script_timeout
    # log_file
    # parsed_result
    # resultfile

    env_vars = filter_out_env_vars(duplicati_env_vars)

    status = env_vars.get('parsed_result').lower()
    if str(env_vars.get('main_action')).lower() == 'backup':
        operation = Operation(backup_name=env_vars.get('backup_name'), begin_time=None, end_time=arrow.now().datetime,
                              duration=None, status=status)
        logger.debug(jsonpickle.encode(operation, unpicklable=False))
        for exp in exporters:
            exp.export(operation)

    # TODO export JSON to GDrive
    # TODO export to Google Sheets
    # TODO export errors to integromat web hook

    # TODO
    exit(0)


def remove_sensitive_info_from_remote_url(remote_url):
    return remote_url


def filter_out_env_vars(env_vars):
    """

    :type env_vars: dict
    :rtype: dict(str, str)

    """
    blacklist = ['passphrase', 'resultfile', 'autoupdater_duplicati_install_root']
    return {k: v for k, v in env_vars.iteritems() if k not in blacklist}


def result_format(operation_result_format):
    # type: (str) -> str

    if operation_result_format.lower() != 'json':
        raise ValueError('{} is not a supported format'.format(operation_result_format))

    return operation_result_format.lower()


def get_duplicati_env_vars():
    # type: () -> dict(str, str)
    return {k.lower().replace('duplicati__', ''): v for k, v in os.environ.iteritems() if
            'duplicati' in str(k).lower()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export duplicati operation')
    parser.add_argument('result_file', type=file, help='File containing the result')
    parser.add_argument('result_format', type=result_format, help='Format that the result is in')

    args = parser.parse_args()

    if args.result_format.lower() == 'json':
        result = json.load(args.result_file)
    else:
        logger.warning('Exporting detailed result from {} format is not yet supported'.format(args.result_format))
        result = None

    duplicati_normalized_env_vars = get_duplicati_env_vars()
    main(result, duplicati_normalized_env_vars)

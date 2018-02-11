class Operation:

    def __init__(self, backup_name, begin_time, end_time, duration, is_dry_run=False, status=''):
        self.backup_name = backup_name
        self.begin_time = begin_time
        self.end_time = end_time
        self.duration = duration  # timedelta
        self.is_dry_run = is_dry_run
        self.status = status

        self.messages = []
        self.warnings = []
        self.errors = []

        self.log_messages = []

# TODO Add one for each of "Backup", "Cleanup", "Restore", or "DeleteAllButN"


class Backup(Operation):

    def __init__(self, backup_storage_info, backup_actions, diff):
        """

        :type diff: Diff
        :type backup_actions: DestinationInteractions
        :type backup_storage_info: BackupStorageInfo
        """
        # top level info
        self.diff = diff
        self.backup_actions = backup_actions
        self.backup_storage_info = backup_storage_info
        """
        :type timedelta
        """

        self.compact_results = None
        self.is_partial_backup = False

        # info about what has changed?

        self.size_opened_files = 0
        self.num_opened_files = 0

        # info about the backup run
        self.size_examined_files = 0  # size of what was found in the source (after files)
        self.num_not_processed_files = 0
        self.num_files_with_error = 0


class Diff:
    """

    Things that have changed on the source compared to the destination.

    """
    def __init__(self, modifications, additions, deletions):
        """

        :type modifications: Change
        :type deletions: Change
        :type additions: Change
        """
        self.modifications = modifications
        self.additions = additions
        self.deletions = deletions  # no size?


class Change:

    def __init__(self, num_files, num_folders, num_symlinks, size_files):
        self.num_files = num_files
        self.num_folders = num_folders
        self.num_symlinks = num_symlinks
        self.size_files = size_files


class DestinationInteractions:

    def __init__(self, num_remote_calls=0, num_bytes_uploaded=0, num_bytes_downloaded=0, num_files_uploaded=0,
                 num_retry_attempts=0, num_folders_created=0, num_files_deleted=0, num_files_downloaded=0):
        """

        :type num_remote_calls: long
        :type num_bytes_uploaded: float
        :type num_bytes_downloaded: float
        :type num_retry_attempts: long
        :type num_folders_created: long
        :type num_files_deleted: long
        :type num_files_uploaded: long
        :type num_files_downloaded: long
        """
        self.num_remote_calls = num_remote_calls  # info on this run
        self.num_bytes_uploaded = num_bytes_uploaded
        self.num_bytes_downloaded = num_bytes_downloaded
        self.num_files_uploaded = num_files_uploaded
        self.num_files_downloaded = num_files_downloaded
        self.num_files_deleted = num_files_deleted
        self.num_folders_created = num_folders_created
        self.num_retry_attempts = num_retry_attempts


class BackupStorageInfo:

    def __init__(self, last_backup_date, destination_info, number_of_backups=None):
        """

        :type destination_info: DestinationInfo
        :type last_backup_date: datetime
        :type number_of_backups: long
        :param last_backup_date:
        :param number_of_backups: number of backups stored
        """
        self.destination_info = destination_info
        self.last_backup_date = last_backup_date  # if this is a successful backup, then this might be the current date
        self.number_of_backups = number_of_backups  # backup_list_count ?


class DestinationInfo:
    def __init__(self, total_quota_bytes=None, free_quota_bytes=None, assigned_quota_bytes=None,
                 number_of_backups=None, num_known_files=None, num_known_file_size_bytes=None,
                 num_unknown_files=None, num_unknown_file_size_bytes=None, name=None, path=None):
        """

        :param total_quota_bytes: the maximum amount of space that can be used for backups ?
        :param free_quota_bytes: remaining space for backups ?
        :param assigned_quota_bytes:
        :param number_of_backups:
        :param num_known_files:
        :param num_known_file_size_bytes:
        :param num_unknown_files:
        :param num_unknown_file_size_bytes:
        """
        self.name = name
        self.path = path
        self.total_quota_bytes = total_quota_bytes
        self.free_quota_bytes = free_quota_bytes  # verify this
        self.assigned_quota_bytes = assigned_quota_bytes
        self.number_of_backups = number_of_backups
        self.num_known_file_count = num_known_files
        self.num_known_file_size_bytes = num_known_file_size_bytes
        self.unknown_file_count = num_unknown_files
        self.num_unknown_file_size_bytes = num_unknown_file_size_bytes

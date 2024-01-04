# https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi
# Thanks to Mateusz Kobos

import filecmp
import os.path

def areDirTreesEqual(dir1, dir2, ignore = []):
    ignore.append('logs.txt')
    # same folder zipped twice results in diff hash - says one guy on SO
    ignore.append('central_data.zip')
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and 
        there were no errors while accessing the directories or files, 
        False otherwise.
   """

    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore)
    if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or \
        len(dirs_cmp.funny_files)>0:
        dirs_cmp.report()
        return False
    (_, mismatch, errors) =  filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch)>0 or len(errors)>0:
        dirs_cmp.report()
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not areDirTreesEqual(new_dir1, new_dir2, ignore):
            dirs_cmp.report()
            return False
    return True

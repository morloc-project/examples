# record DiskUsageConfig where
#   --' true: -h
#   humanReadable :: Bool
#   --' true: -a/--all
#   includeHidden :: Bool
#   --' default: -1
#   depth :: Int




"""
Directory Statistics - Fundamental Functions
Each function does one clear thing and can be composed together
"""
import os
from typing import List, Tuple, Optional


# ============================================================================
# File System Query Functions
# ============================================================================

def get_file_size(filepath: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Size in bytes, or 0 if file cannot be accessed
    """
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0


def is_hidden(name: str) -> bool:
    """
    Check if a file or directory name is hidden (starts with .).
    
    Args:
        name: Filename or directory name
    
    Returns:
        True if hidden, False otherwise
    """
    return name.startswith('.')


def get_files_in_directory(directory: str, include_hidden: bool = False) -> List[str]:
    """
    Get all files in a directory (non-recursive).
    
    Args:
        directory: Directory path to scan
        include_hidden: Include hidden files (starting with .)
    
    Returns:
        List of file paths
    """
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            if include_hidden or not is_hidden(entry.name):
                files.append(entry.path)
    return files


def walk_directory(path: str, include_hidden: bool = False, 
                   max_depth: int = -1) -> List[Tuple[str, List[str], List[str]]]:
    """
    Walk a directory tree, yielding (dirpath, dirnames, filenames) tuples.
    
    Args:
        path: Root directory path
        include_hidden: Include hidden files and directories
        max_depth: Maximum depth to traverse (-1 for unlimited)
    
    Returns:
        List of (dirpath, dirnames, filenames) tuples
    """
    results = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        # Check depth
        if max_depth >= 0:
            current_depth = dirpath[len(path):].count(os.sep)
            if current_depth > max_depth:
                continue
        
        # Filter hidden directories
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not is_hidden(d)]
        
        # Filter hidden files
        if not include_hidden:
            filenames = [f for f in filenames if not is_hidden(f)]
        
        results.append((dirpath, dirnames, filenames))
    
    return results


def has_extension(filename: str, extension: str) -> bool:
    """
    Check if a filename has a specific extension.
    
    Args:
        filename: Name of the file
        extension: Extension to check (e.g., ".py")
    
    Returns:
        True if filename ends with extension
    """
    return filename.endswith(extension)


# ============================================================================
# Filtering Functions
# ============================================================================

def filter_by_extension(filepaths: List[str], extension: str) -> List[str]:
    """
    Filter a list of file paths by extension.
    
    Args:
        filepaths: List of file paths
        extension: Extension to filter by (e.g., ".py")
    
    Returns:
        Filtered list of file paths
    """
    return [f for f in filepaths if has_extension(f, extension)]


def filter_hidden(filepaths: List[str]) -> List[str]:
    """
    Filter out hidden files from a list.
    
    Args:
        filepaths: List of file paths
    
    Returns:
        List with hidden files removed
    """
    return [f for f in filepaths if not is_hidden(os.path.basename(f))]


# ============================================================================
# Sorting Functions
# ============================================================================

def sort_by_name(filepaths: List[str], reverse: bool = False) -> List[str]:
    """
    Sort file paths alphabetically by name.
    
    Args:
        filepaths: List of file paths
        reverse: Sort in reverse order
    
    Returns:
        Sorted list of file paths
    """
    return sorted(filepaths, reverse=reverse)


def sort_by_size(filepaths: List[str], reverse: bool = False) -> List[str]:
    """
    Sort file paths by file size.
    
    Args:
        filepaths: List of file paths
        reverse: Sort in reverse order (largest first if True)
    
    Returns:
        Sorted list of file paths
    """
    return sorted(filepaths, key=get_file_size, reverse=reverse)


# ============================================================================
# Aggregation Functions
# ============================================================================

def calculate_total_size(filepaths: List[str]) -> int:
    """
    Calculate the total size of multiple files.
    
    Args:
        filepaths: List of file paths
    
    Returns:
        Total size in bytes
    """
    return sum(get_file_size(f) for f in filepaths)


def get_all_files_recursive(path: str, include_hidden: bool = False, 
                            max_depth: int = -1) -> List[str]:
    """
    Get all files in a directory tree.
    
    Args:
        path: Root directory path
        include_hidden: Include hidden files
        max_depth: Maximum depth to traverse
    
    Returns:
        List of all file paths found
    """
    all_files = []
    for dirpath, _, filenames in walk_directory(path, include_hidden, max_depth):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))
    return all_files


# ============================================================================
# Formatting Functions
# ============================================================================

def format_bytes_human_readable(size_bytes: int) -> str:
    """
    Format a byte size as human-readable string (KB, MB, GB, etc.).
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.50 MB")
    """
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def format_file_list(filepaths: List[str], show_size: bool = False) -> str:
    """
    Format a list of file paths as a string.
    
    Args:
        filepaths: List of file paths
        show_size: Include file sizes in output
    
    Returns:
        Formatted string with one file per line
    """
    if not show_size:
        return '\n'.join(filepaths)
    
    lines = []
    for filepath in filepaths:
        size = get_file_size(filepath)
        size_str = format_bytes_human_readable(size)
        lines.append(f"{filepath} ({size_str})")
    return '\n'.join(lines)


# ============================================================================
# High-Level Composed Functions (examples of composition)
# ============================================================================

def disk_usage(path: str, human_readable: bool = True,
               include_hidden: bool = False, depth: int = -1) -> str:
    """
    Calculate total disk usage of a directory.
    Composed from: get_all_files_recursive, calculate_total_size, format_bytes_human_readable
    """
    files = get_all_files_recursive(path, include_hidden, depth)
    total_bytes = calculate_total_size(files)
    
    if human_readable:
        return format_bytes_human_readable(total_bytes)
    return str(total_bytes)


def list_by_extension(directory: str, extension: Optional[str] = None,
                     sort_by_size_flag: bool = False, reverse: bool = False) -> List[str]:
    """
    List files in a directory, optionally filtered by extension.
    Composed from: get_files_in_directory, filter_by_extension, sort_by_name, sort_by_size
    """
    files = get_files_in_directory(directory, include_hidden=False)
    
    if extension is not None:
        files = filter_by_extension(files, extension)
    
    if sort_by_size_flag:
        files = sort_by_size(files, reverse)
    else:
        files = sort_by_name(files, reverse)
    
    return files

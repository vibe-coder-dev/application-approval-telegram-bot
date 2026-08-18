"""
Tests for file handling utilities
"""
import pytest
import os
import tempfile
from pathlib import Path


class TestFileHandler:
    """Test file handling functions"""
    
    @pytest.fixture(autouse=True)
    def setup_test_directories(self):
        """Setup test directories"""
        # Create test upload directory
        Path('uploads_test').mkdir(exist_ok=True)
        Path('uploads_test/photos').mkdir(exist_ok=True)
        Path('uploads_test/documents').mkdir(exist_ok=True)
        Path('uploads_test/files').mkdir(exist_ok=True)
        
        yield
        
        # Cleanup
        import shutil
        if Path('uploads_test').exists():
            shutil.rmtree('uploads_test')
    
    def test_ensure_upload_dir(self):
        """Test ensure_upload_dir function"""
        from bot.utils.file_handler import ensure_upload_dir
        from bot.config.settings import settings
        
        # Temporarily change upload dir
        original_upload_dir = settings.UPLOAD_DIR
        settings.UPLOAD_DIR = 'uploads_test'
        
        try:
            ensure_upload_dir()
            
            # Check directories exist
            assert Path('uploads_test').exists()
            assert Path('uploads_test/photos').exists()
            assert Path('uploads_test/documents').exists()
            assert Path('uploads_test/files').exists()
        finally:
            settings.UPLOAD_DIR = original_upload_dir
    
    def test_generate_filename(self):
        """Test generate_filename function"""
        from bot.utils.file_handler import generate_filename
        
        # Test without extension
        filename1 = generate_filename()
        assert len(filename1) > 0
        assert '_' in filename1
        
        # Test with extension
        filename2 = generate_filename('.txt')
        assert filename2.endswith('.txt')
        assert '_' in filename2
        
        # Test with extension without dot
        filename3 = generate_filename('txt')
        assert filename3.endswith('.txt')
    
    def test_save_and_delete_file(self):
        """Test save_file and delete_file functions"""
        from bot.utils.file_handler import save_file, delete_file, get_file_path
        from bot.config.settings import settings
        
        # Temporarily change upload dir
        original_upload_dir = settings.UPLOAD_DIR
        settings.UPLOAD_DIR = 'uploads_test'
        
        try:
            # Test data
            test_data = b"Test file content"
            test_filename = "test_file.txt"
            
            # Save file
            file_path, saved_filename = save_file(
                test_data,
                test_filename,
                "document"
            )
            
            # Check file was saved
            assert Path(file_path).exists()
            assert saved_filename.startswith('202')  # Should start with date
            
            # Check file content
            with open(file_path, 'rb') as f:
                content = f.read()
            assert content == test_data
            
            # Test get_file_path
            retrieved_path = get_file_path(saved_filename)
            assert retrieved_path is not None
            
            # Delete file
            result = delete_file(file_path)
            assert result is True
            
            # Check file was deleted
            assert not Path(file_path).exists()
            
        finally:
            settings.UPLOAD_DIR = original_upload_dir
    
    def test_save_photo(self):
        """Test saving photo file"""
        from bot.utils.file_handler import save_file
        from bot.config.settings import settings
        
        # Temporarily change upload dir
        original_upload_dir = settings.UPLOAD_DIR
        settings.UPLOAD_DIR = 'uploads_test'
        
        try:
            # Test photo data
            photo_data = b"Fake photo data"
            
            # Save photo
            file_path, saved_filename = save_file(
                photo_data,
                "test_photo.jpg",
                "photo"
            )
            
            # Check file was saved in photos directory
            assert 'photos' in file_path
            assert Path(file_path).exists()
            
        finally:
            settings.UPLOAD_DIR = original_upload_dir
    
    def test_get_file_info(self):
        """Test get_file_info function"""
        from bot.utils.file_handler import get_file_info, save_file
        from bot.config.settings import settings
        
        # Temporarily change upload dir
        original_upload_dir = settings.UPLOAD_DIR
        settings.UPLOAD_DIR = 'uploads_test'
        
        try:
            # Create a test file
            test_data = b"Test content"
            file_path, _ = save_file(test_data, "test.txt", "file")
            
            # Get file info
            info = get_file_info(file_path)
            
            assert info['exists'] is True
            assert info['path'] == file_path
            assert info['name'] == 'test.txt' or info['name'].endswith('.txt')
            assert info['size'] == len(test_data)
            
            # Test non-existent file
            info_none = get_file_info("non_existent_file.txt")
            assert info_none['exists'] is False
            
        finally:
            settings.UPLOAD_DIR = original_upload_dir
    
    def test_validate_file_size(self):
        """Test validate_file_size function"""
        from bot.utils.file_handler import validate_file_size
        
        # Test valid size
        assert validate_file_size(1024) is True  # 1KB
        assert validate_file_size(10 * 1024 * 1024) is True  # 10MB
        
        # Test too large
        assert validate_file_size(11 * 1024 * 1024) is False  # 11MB
        
        # Test custom max size
        assert validate_file_size(5 * 1024 * 1024, max_size=5 * 1024 * 1024) is True
        assert validate_file_size(6 * 1024 * 1024, max_size=5 * 1024 * 1024) is False
    
    def test_allowed_extensions(self):
        """Test allowed extensions"""
        from bot.utils.file_handler import get_allowed_extensions, is_allowed_extension
        
        allowed = get_allowed_extensions()
        
        # Test some allowed extensions
        assert '.jpg' in allowed
        assert '.png' in allowed
        assert '.pdf' in allowed
        assert '.doc' in allowed
        assert '.txt' in allowed
        
        # Test is_allowed_extension
        assert is_allowed_extension('.jpg') is True
        assert is_allowed_extension('.JPG') is True  # Case insensitive
        assert is_allowed_extension('.exe') is False
        assert is_allowed_extension('.unknown') is False

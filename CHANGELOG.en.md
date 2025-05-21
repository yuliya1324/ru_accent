# Changelog

## [0.1.6] - 2025-05-21

Changes by Danslav Slavenskoj

### Added
- Support for TensorFlow 2.15+ and Keras 3.x
- Custom implementation of the russtress Accent class for modern compatibility
- Test script to verify functionality with modern TensorFlow

### Changed
- Updated dependency requirements in setup.py
- Improved error handling for TensorFlow/Keras compatibility
- Suppressed verbose TensorFlow warnings
- Updated documentation with new compatibility information

### Fixed
- Model loading compatibility with Keras 3.x
- Fixed boolean type handling for numpy arrays
- Improved handling of model architecture changes in TensorFlow 2.x

## [0.1.5] - Initial Release

- Initial release of ru_accent_poet
- Support for analyzing Russian text and adding stress marks
- Original implementation with TensorFlow 1.x compatibility
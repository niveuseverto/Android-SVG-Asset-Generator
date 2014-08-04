Android SVG Asset Generator
----
Future proof your assets and save time! 

Create / find once and don't worry about DPI buckets.

This tool allows you to use SVG files for your Android apps image resources. 

SVG images are scaled and put into appropriate folders for android and the 9 patch is applied.

Generating Images
----
1. Put SVG files to `assets` directory, near Android `res` directory.
2. Run `process_assets.py`.
	
Source Image Info
----
The document size on your SVG files should reflect the image size at 160dpi.

To add a 9patch to generated images, add a hidden layer called 9patch see tag.svg for an example

Requirements
----
* Linux, OS X, Windows
* Inkscape
* Python
* PIL

Next
----
* Command line parameters for:
    1. Changing of document DPI
    2. Setting assets folder
    3. Setting resource folder
    4. Disabling one or more of Android Densities
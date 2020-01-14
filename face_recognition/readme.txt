face recognition tutorial :
https://towardsdatascience.com/building-k-pop-idol-identifier-with-amazon-rekognition-92302442d763
code:
https://github.com/tthustla/twice_recognition

How to use this tool:
Create a folder 'fonts' and copy the 'Arial*.ttf' files into it, from ~/Windows/Fonts folder.

Create a folder 'credentials' two levels above and put your AWS credentials in aws.csv file.
('../../credentials/aws.csv')

Create a root folder called 'images'.
Optionally, create a subfolder for each person. 
Load 3 or 4 jpg/png pictures of every person:
  The file name should be of the form Rajaram_1.jpg, Rajaram_2.jpg etc.
  The part before the underscore will be used for labelling while training.

Run the program create_collection.py:
> python create_collection  collection_name
This has to be done only once.

Upload all the images recursively to the collection:
> python indexer.py  [root_folder_name]  [collection_name]

Recognize faces present in a target file named test_file_name:
> python recognizer.py  test_file_name  [collection_name]

To quickly test face detection capabilities:
> python detect_faces.py  source_file_name   
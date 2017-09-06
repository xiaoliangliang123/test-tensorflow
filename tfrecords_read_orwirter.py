import tensorflow as tf
import matplotlib.image as mpimg


1. #convert csv to tfrecords
train_frame = pd.read_csv('./train.csv')
train_label_frame = train_frame.pop(item="label")
train_image = train_frame.values
train_label = train_label_frame.values

writer = tf.python_io.TFRecordWriter("./train.tfrecords")
for i in range(train_image.shape()[0]):
	image_raw = train_image[i].tostring()
	example = tf.train.Example(
		features = tf.train.Features(
			feature = {
				"image" : tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_raw])),
				"label" : tf.train.Feature(int64_list=tf.train.Int64List(value=[train_label[i]]))
			}
		)
	)
	writer.write(record=example.SerializeToString())
writer.close()

2 # convert imag to tfrecords
filenames = tf.train.match_filenames_once(".\data\*.png")
file_queue = tf.train.string_input_producer(filenames, shuffle=False, num_epochs=3)

writer = tf.python_io.TFRecordWriter("img_demo.tfrecords")
for f in filenames:
	img = mpimg.imread(f)
	img_raw = img.tostring()
	example = tf.train.Example(
		features = tf.train.Features(
			feature = {
				"image" : tf.train.Feature(bytes_list=tf.BytesList(value = [img_raw])),
				"label" : tf.train.Feature(int64_list = tf.tain.Int64List(value=[lable])
			}
		)
	)
	
	writer.write(record = example.SerializeToString())
	
writer.close()




3. #Read tfrecords

reader = tf.TFRecordReader()
filename = tf.train.match_filenames_once('img_demo.tfrecords')
filequeue = tf.train.string_input_producer(filename, shuffle=False, num_epochs=3)

reader = tf.TFRecordReader()
_, serialized_record = reader.read(filequeue)

features = tf.parse_single_example(
	serialized_record,
	features = {
		'image': tf.FixedLenFeature([], tf.string),
		"label": tf.FixedLenFeature([], tf.int64)
	}
)

images = tf.decode_raw(features['image'])
label = tf.cast(features['label'], tf.int32)

init_op = tf.local_variables_initializer()

with tf.Session() as sess:
	sess.run(init_op)
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runers(sess=sess, coord=coord)
	
	for i in range(10):
		image, label = sess.run([images, label])
	
	coord.request_stop()
	coord.join(threads)



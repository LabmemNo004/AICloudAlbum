import shutil

from django.test import TestCase

# Create your tests here.
from django.test import TestCase,Client
from Album.views import *
# testing face module
from AI.FaceDetect.FaceDetect import FaceRecogPrepared
from AI.FaceDetect.VisualizeDetect import VisualizeBlocks
import Album.models as models
import os
# Create your tests here.

# testing delete_select_image module

def setUp(client):
    compress_dir = os.path.join(store_dir, "compress_imgs")
    src_dir = os.path.join(store_dir, "face_img")
    for now_img in os.listdir(store_dir):
        if "." in now_img:
            os.remove(os.path.join(store_dir, now_img))
    for now_img in os.listdir(compress_dir):
        if "." in now_img:
            os.remove(os.path.join(compress_dir, now_img))
    for now_img in os.listdir(src_dir):
        shutil.copy(os.path.join(src_dir, now_img), os.path.join(store_dir, now_img))
        shutil.copy(os.path.join(src_dir, now_img), os.path.join(compress_dir, now_img))

    models.Tag(tag="None").save()
    file = open("/Users/tanzhongyu/AICloudAlbum/AI/ImgClass_new/config/tags.txt")
    line = file.readline()
    while line:
        models.Tag(tag=line).save()
        line = file.readline()

    fake_id = hash_code("root", salt="user")

    new_user = models.User(name="admin", phone="root", pwd=hash_code("root") + "-" + "root",
                           max_capacity=0, fake_id=fake_id)
    new_user.save()

    new_ini_folder = models.Folder(name="ALL", user_id=new_user.phone,
                                   cnt=0, total_size=0.0,
                                   create_time=datetime.datetime.now(),
                                   modify_time=datetime.datetime.now(),
                                   )
    new_ini_folder.save()
    new_ini_folder.fake_name = hash_code(str(new_ini_folder.pk), salt="neko_folder")
    new_ini_folder.save()

    NoneTag = models.Tag.objects.get(tag="None")

    new_img = models.Picture(name="empty", type="png", upload_time=datetime.datetime.now(),
                             size=0, height=0, width=0, is_tag=False, is_face=False,
                             folder_id=new_ini_folder.pk, tag_id=NoneTag.pk, user_id=new_user.phone)

    new_img.save()
    new_img.fake_name = hash_code(str(new_img.pk), salt="neko_img")
    new_img.save()


    data = {
        "phone": '13600000000',
        "name": "test1",
        "pwd": "test1",
        "re_pwd": "test1",
    }
    response = client.post("/signup/", data)


    phone = '13600000000'
    now_user = models.User.objects.get(name="test1")

    nowFolder = models.Folder.objects.get(user_id=phone, name="ALL")

    NoneTag = models.Tag.objects.get(tag="None")

    for i in range(62):
        img_path = os.path.join(store_dir, "face_" + str(i + 1) + ".jpg")
        now_size = os.path.getsize(img_path) / 1024 / 1024
        with Image.open(img_path) as img:
            h, w = img.size[0], img.size[1]
        new_img = models.Picture(name="face" + str(i + 1), type="jpg", upload_time=datetime.datetime.now(),
                                 size=now_size, height=h, width=w, is_tag=False, is_face=False,
                                 folder_id=nowFolder.pk, tag_id=NoneTag.pk, user_id=phone)

        new_img.save()
        new_img.fake_name = hash_code(str(new_img.pk), salt="test_img")
        new_img.save()

        now_img_name = str(new_img.fake_name) + ".jpg"
        compress_img_path_old = os.path.join(store_compress_dir, "face_" + str(i + 1) + ".jpg")
        compress_img_path_new = os.path.join(store_compress_dir, now_img_name)
        img_path_new = os.path.join(store_dir, now_img_name)
        os.rename(img_path, img_path_new)
        os.rename(compress_img_path_old, compress_img_path_new)


def tearDown():
    compress_dir = os.path.join(store_dir, "compress_imgs")
    for now_img in os.listdir(store_dir):
        if "." in now_img:
            os.remove(os.path.join(store_dir, now_img))
    for now_img in os.listdir(compress_dir):
        if "." in now_img:
            os.remove(os.path.join(compress_dir, now_img))



class TestDeleteSelectImage1(TestCase):
    def setUp(self):
        print("Test Case 1 of Delete Select Image \n")
        print('setUp......\n')
        self.client=Client()
        setUp(self.client)


    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has login (valid)
        # folder_fake_name is the All folder's fake name (valid)
        # select_image_list (all of the 4 images are in the All folder)

        # prepare data needed
        phone= '13600000000'
        folder=models.Folder.objects.get(user_id=phone, name="ALL")
        pics=models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete=[]

        for i , pic in enumerate(pics):
            if i>3:
                break
            pic_delete.append(pic.fake_name)
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name=folder.fake_name
        url="/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:T")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code=response.status_code
        content=response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))




class TestDeleteSelectImage2(TestCase):

    def setUp(self):
        print("Test Case 2 of Delete Select Image \n")
        print('setUp......\n')
        self.client = Client()
        setUp(self.client)

    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has not login (not valid)

        # prepare data needed
        phone = '13600000000'
        folder = models.Folder.objects.get(user_id=phone, name="ALL")
        pics = models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete = []
        response = self.client.post("/loginout/")

        for i, pic in enumerate(pics):
            if i > 3:
                break
            pic_delete.append(pic.fake_name)
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name = folder.fake_name
        url = "/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:F")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code = response.status_code
        content = response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))
        print("link to:{}\n".format(response.url))



class TestDeleteSelectImage3(TestCase):
    def setUp(self):
        print("Test Case 3 of Delete Select Image \n")
        print('setUp......\n')
        self.client=Client()
        setUp(self.client)


    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has login (valid)
        # folder_fake_name is the All folder's fake name (valid)
        # select_image_list (empty)

        # prepare data needed
        phone= '13600000000'
        folder=models.Folder.objects.get(user_id=phone, name="ALL")
        pics=models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete=[]
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name=folder.fake_name
        url="/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:T")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code=response.status_code
        content=response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))



class TestDeleteSelectImage4(TestCase):
    def setUp(self):
        print("Test Case 4 of Delete Select Image \n")
        print('setUp......\n')
        self.client=Client()
        setUp(self.client)


    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has login (valid)
        # folder_fake_name is the All folder's fake name (valid)
        # select_image_list (3 images are in the All folder and 1 image fake name has invalid char)

        # prepare data needed
        phone= '13600000000'
        folder=models.Folder.objects.get(user_id=phone, name="ALL")
        pics=models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete=[]
        for i, pic in enumerate(pics):
            if i > 3:
                break
            pic_delete.append(pic.fake_name)
        pic_delete[0]=pic_delete[0][:-1]+"#"
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name=folder.fake_name
        url="/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:T")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code=response.status_code
        content=response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))


class TestDeleteSelectImage5(TestCase):
    def setUp(self):
        print("Test Case 5 of Delete Select Image \n")
        print('setUp......\n')
        self.client=Client()
        setUp(self.client)


    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has login (valid)
        # folder_fake_name is the All folder's fake name (valid)
        # select_image_list (3 images are in the All folder and 1 image fake name is not in the database)

        # prepare data needed
        phone= '13600000000'
        folder=models.Folder.objects.get(user_id=phone, name="ALL")
        pics=models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete=[]
        for i, pic in enumerate(pics):
            if i > 3:
                break
            pic_delete.append(pic.fake_name)
        pic_delete[0]=pic_delete[0][:-1]+"f"
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name=folder.fake_name
        url="/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:T")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code=response.status_code
        content=response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))



class TestDeleteSelectImage6(TestCase):
    def setUp(self):
        print("Test Case 6 of Delete Select Image \n")
        print('setUp......\n')
        self.client=Client()
        setUp(self.client)


    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_delete_select_images(self):
        # phone is 13600000000 (valid)
        # user has login (valid)
        # folder_fake_name is the All folder's fake name (valid)
        # select_image_list (all 4 image fake name are not in the database)

        # prepare data needed
        phone= '13600000000'
        folder=models.Folder.objects.get(user_id=phone, name="ALL")
        pics=models.Picture.objects.filter(user_id=phone, folder_id=folder.id)
        pic_delete=[]
        for i, pic in enumerate(pics):
            if i > 3:
                break
            pic_delete.append(pic.fake_name)
        pic_delete[0]=pic_delete[0][:-3]+"abc"
        pic_delete[1] = pic_delete[1][:-3] + "abc"
        pic_delete[2] = pic_delete[2][:-3] + "abc"
        pic_delete[3] = pic_delete[3][:-3] + "abc"
        data = {
            "img_name": pic_delete
        }

        # generate folder fake name and url
        folder_fake_name=folder.fake_name
        url="/delete_select_img/" + folder_fake_name + "/"

        # show input value
        print("Input:")
        print("phone:{}".format(phone))
        print("isLogin:T")
        print("select_image_list:{}".format(pic_delete))
        print("folder_fake_name:{}\n".format(folder_fake_name))

        # test delete_select_image function
        response = self.client.post(url, data)
        status_code=response.status_code
        content=response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))




# testing face module

upload_imgs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "AICloudAlbum/upload_imgs/face_img")

class FaceDetectTestCase1(TestCase):

    def setUp(self):
        print("Test Case 1 of Face Detect \n")
        print('setUp......\n')
        self.client = Client()
        setUp(self.client)

    def tearDown(self):
        print('tearDown......\n')
        tearDown()


    def test_user(self):
        self.maxDiff=None
        post_signup_data={
            "phone": '13600000000',
            "name": "test1",
            "pwd": "test1",
            "re_pwd": "test1"
        }
        post_login_data = {
            "phone": '13600000000',
            "pwd": "test1",
        }
        response = self.client.post('/signup', data=post_signup_data,
                                    content_type='application/json')
        #self.assertEqual(response, True)
        response = self.client.post('/login', data=post_login_data,
                                    content_type='application/json')
        #self.assertEqual(response, True)
        # show input value
        print("Input:")
        print("phone:{}".format(post_login_data['phone']))
        print("isLogin:T")

        status_code = response.status_code
        content = response.content

        # show output value
        print("Output:")
        print("status:{}".format(status_code))
        print("content:{}\n".format(content))


class FaceDetectTestCase2(TestCase):
    # 测试人脸识别FaceDetect模块2:

    def setUp(self):
        print("Test Case 2 of Face Detect \n")
        print('setUp......\n')
        self.client = Client()
        setUp(self.client)

    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_face(self):
        user = {
            "phone": '13600000000',
            "name": "test1",
            "pwd": "test1",
        }
        filepath = upload_imgs_dir + "/face_9.jpg"
        isFace, face_locations, recognized_faces,saved_face_img_name = FaceRecogPrepared(filepath, user['phone'], True)
        # 展示结果
        print("Input:")
        print("imageToBeDetected:"+filepath)
        print("Output:")
        print("isFace:" + str(isFace))
        print("Face Locations:")
        print(face_locations)
        print("Face Recognitions:")
        print(recognized_faces)
        print("\n")
        VisualizeBlocks(filepath, face_locations)

        self.assertEqual(isFace, True)
        self.assertEqual(len(face_locations) == 0, False)
        for recog in recognized_faces:
            self.assertEqual(recog == 'Not matched', False)


class FaceDetectTestCase3(TestCase):
    # 测试人脸识别FaceDetect模块3:

    def setUp(self):
        print("Test Case 3 of Face Detect \n")
        print('setUp......\n')
        self.client = Client()
        setUp(self.client)

    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_face(self):
        user = {
            "phone": '13600000000',
            "name": "test1",
            "pwd": "test1",
        }
        img_list=["/face_2.jpg", "/face_1.jpg", "/face_3.jpg"]
        for img_name in img_list:
            filepath = upload_imgs_dir + img_name
            isFace, face_locations, recognized_faces, saved_face_img_name = FaceRecogPrepared(filepath, user['phone'],
                                                                                              True)
            # 展示结果
            print("Input:")
            print("imageToBeDetected:" + filepath)
            print("Output:")
            print("isFace:" + str(isFace))
            print("Face Locations:")
            print(face_locations)
            print("Face Recognitions:")
            print(recognized_faces)
            print("\n")
            VisualizeBlocks(filepath, face_locations)

            self.assertEqual(isFace, True)
            self.assertEqual(len(face_locations) == 0, False)



class FaceDetectTestCase4(TestCase):
    # 测试人脸识别FaceDetect模块4:

    def setUp(self):
        print("Test Case 4 of Face Detect \n")
        print('setUp......\n')
        self.client = Client()
        setUp(self.client)

    def tearDown(self):
        print('tearDown......\n')
        tearDown()

    def test_face3(self):
        user = {
            "phone": '13600000000',
            "name": "test1",
            "pwd": "test1",
        }
        testNum = 20
        for i in range(testNum):
            img_name="/face_"+str(i+20)+".jpg"
            filepath = upload_imgs_dir + img_name
            isFace, face_locations, recognized_faces, saved_face_img_name = FaceRecogPrepared(filepath, user['phone'],                                                                                    True)
            # 展示结果
            print("Input:")
            print("imageToBeDetected:" + filepath)
            print("Output:")
            print("isFace:" + str(isFace))
            print("Face Locations:")
            print(face_locations)
            print("Face Recognitions:")
            print(recognized_faces)
            print("\n")
            VisualizeBlocks(filepath, face_locations)


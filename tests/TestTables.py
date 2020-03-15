import user_Test 
import collab_Test
import youtube_video_Test
import meal_Test
import workout_Test



user_Test.GetAll()
user_Test.GetSingle("1")
user_Test.Post()
user_Test.Delete("1")
user_Test.Put("1")
user_Test.PostLogin()
print(user_Test.userPC , "/6 tests passed")

collab_Test.GetAll()
collab_Test.GetSingle("1")
collab_Test.Delete()
collab_Test.Post()
collab_Test.Put("50")
print(collab_Test.collabPC , "/5 tests passed")

youtube_video_Test.GetAll()
youtube_video_Test.GetSingle("1")
youtube_video_Test.Delete("50")
youtube_video_Test.Post()
youtube_video_Test.Put("50")
print(youtube_video_Test.youtubePC , "/5 tests passed")

meal_Test.GetAll()
meal_Test.GetSingle("11")
meal_Test.Delete("11")
meal_Test.Post()
meal_Test.Put("11")
print(meal_Test.mealPC , "/5 tests passed")

workout_Test.GetAll()
workout_Test.GetSingle("1")
workout_Test.Delete("10")
workout_Test.Post()
workout_Test.Put("10")
print(workout_Test.workoutPC , "/5 tests passed")


from datetime import datetime, date
from app import app, db
from models.user import UserModel
from models.movement import MovementModel
from models.post import PostModel
from models.session import SessionModel
from models.user_session import UserSessionModel
from models.parq import ParqModel



with app.app_context():

    try:
        print('Creating our database....')
        db.drop_all()
        db.create_all()

        print('Seeding the database!')

    # User seeding
        bertie = UserModel(username="bertie", email="bertiebert@bert.com", password="password", is_admin="True")
        bertie.save()
        freddie = UserModel(username="freddie", email="freddiefred@fred.com", password="password", is_admin="false")
        freddie.save()
        percy = UserModel(username="percy", email="percyperc@perc.com", password="password", is_admin="false")
        percy.save()
        betty = UserModel(username="betty", email="bettybett@bett.com", password="password", is_admin="false")
        betty.save()

  #   # Movement seeding
        squatpulses = MovementModel(name="Squat Pulses", descriptionOne="From a standing position and your knees off lock - remember to keep your ears, shoulders and hip in line and your spine in neutral and brace your abdominals", descriptionTwo="From this position slowly lower into a squat position", descriptionThree="During the lowering movement make sure your heels remain flat and in contact withthe ground - this downward movement is about hinging at the hip and sticking your bottom out imagining you are about to sit onto the toilet.", descriptionFour="Stay in the squat position, gently pulse your legs in an up and down motion - make sure to maintain the tension in your thigh muscles throughout Be sure to keep the abdominals braced throughout", image="https://womensfitness.co.uk/wp-content/uploads/sites/3/2020/12/01-Squat.jpg", type="Strength", equipment="bodyweight", video="https://www.youtube.com/embed/usxdXASMo1Q?si=vzrZEY-icqs3-bx9", adaption="Slightly lowering into the squat and not lowering too deep will reduce the intensity of the exercise and allow for a gentler movement OR a Progression - The deeper the squat (the lower you go) the greater the intensity of the exercise - make sure to keep your feet flat on the floor and let this gauge how low you go", user_id=bertie.id)
        squatpulses.save()
        clamshells = MovementModel(name="Clam Shells", descriptionOne="This exercise will help you to activate your gluteus medius (one part (muscle) of your buttocks) - It is essential to remain a regular breathing technique throughout the whole movement",descriptionTwo="Lying on your side - place your hand on your hip", descriptionThree="With your hips and knees flexed, externally rotate your upper hip (mimicking the movement of a clam shell opening)",descriptionFour="Make sure to keep your feet together - you should feel your bottom activate", image="https://samarpanphysioclinic.com/wp-content/uploads/2022/11/Clamshell.webp", type="Strength", equipment="bodyweight", video="https://www.youtube.com/embed/XPRze2hO0ek?si=mg4LvpbnLKPxc6lr", adaption="Lift your upper foot slightly away from the lower foot to intensify the exercise", user_id=bertie.id)
        clamshells.save()
        glutebridge = MovementModel(name="Glute Bridge", descriptionOne="This exercise activates the gluteus maximus (a part (muscle) of the buttocks) - It is essential to remain a regular breathing technique throughout the whole movement",descriptionTwo="Lying on your back with your hips and knees bent and feet flat on the floor", descriptionThree="Then imagine you have a coin placed where the lower limits of the bottom meets the upper limits of the thigh - then make sure that this ‘coin’ isn’t dropped. Do this by squeezing your buttocks, not by extending (opening up) your hips",descriptionFour="It is really important not to overextend (push your hips to high) - concentrate on activating the buttocks but keeping your pelvis and spine in neutral (in line) and repeat", image="https://media.istockphoto.com/id/1673188303/vector/young-women-doing-glute-bridges-exercise.jpg?s=612x612&w=0&k=20&c=7iad8UPHN-BR2IHcq6D4cwnu_Oz0x6tM85N9CMvKOwE=", type="Strength", equipment="bodyweight", video="https://www.youtube.com/embed/EF2w6V1gP8g?si=tnbiYs4hY6rXycNs", adaption="Lift one foot from the ground and keep it lifted throughout the movement", user_id=bertie.id)
        glutebridge.save()
        heelslide = MovementModel(name="Heel Slide", descriptionOne="It is essential to remain a regular breathing technique throughout the entire movement",descriptionTwo="Lie in a crook-lying position with your spine in neutral (lying on your back with your knees bent)", descriptionThree="Slowly straighten one leg with your heel sliding along the ground - to facilitate the movement this exercise is best performed on a slippery surface, or even using shiny material on carpet",descriptionFour="This movement the pelvis tilts anteriorly - increasing lumbar lordosis (the lower back arches and lifts off the ground). If this occurs, stop the movement and bend the hip and knee to regain neutral position.", image="https://workoutlabs.com/wp-content/uploads/watermarked/Lying_Heel_Slides_F.png", type="Strength", equipment="bodyweight", video="https://www.youtube.com/embed/0d3s0FW9ESU?si=5yPySasbxq0kngSl", adaption="Lift one foot from the ground and keep it lifted throughout the movement", user_id=betty.id)
        heelslide.save()
        birddog = MovementModel(name="Bird Dog", descriptionOne="The main aim of a four-point kneeling exercise such as bird dog is to maintain stability during the movement of limbs away and towards your body. It is essential to remain a regular breathing technique throughout the whole movement",descriptionTwo="Start in a stable position with an even weight distribution through your hands and feet", descriptionThree="Keeping your hips level, gently extend your leg behind until it is parallel to the ground (by lifting your limb from the floor your body becomes less stable and your stabilising muscles work harder maintain balance)",descriptionFour="Then return your leg to its original position and repeat on the other leg. Be sure to engage your core throughout the movement and use your glutes to drive the leg backwards", image="https://img.freepik.com/premium-vector/bird-dog-exercise-silhouette-workout-training-women-illustration_591091-407.jpg", type="Strength", equipment="bodyweight", video="https://www.youtube.com/embed/TM3N33i_-eY?si=dRBR6u0tsaJzjCML", adaption="Lift your opposite hand at the same time as your leg, making sure to keep your hips level throughout", user_id=bertie.id)
        birddog.save()
        fastfeet = MovementModel(name="Fast Feet", descriptionOne="Fast feet is a great full body cardio exercise that uses lots of different muscle groups",descriptionTwo="Standing in an upright position - making sure to keep you eyes up towards the horizon", descriptionThree="Simply move your feet as fast as possible, keeping your hips low and your feet quite close to the ground",descriptionFour="Be sure to engage your core throughout by drawing your belly button up towards your spine", image="https://i.pinimg.com/originals/fd/2e/0a/fd2e0aebc51342db7a3751daa9206f7b.jpg", type="Cardio", equipment="bodyweight", video="https://www.youtube.com/embed/NfQea8-1hmI?si=j_ECHnFyhMCASM4R", adaption="To progress this further adopt a deeper position by lowering your hips closer to the ground OR increase the speed at which you move your feet", user_id=bertie.id)
        fastfeet.save()

    # Post seeding..
        keepgoing = PostModel(content="Attitude is the little thing that makes a big difference - Winston Churchill", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="Some times on life’s ride you may fall, dust right off, get back up, give it all", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="You can’t cross the sea merely by standing and staring at the water - Rabindranath Tagore", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="Be there for others, but never leave yourself behind - Dodinsky.", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="Did you know? There are only 10 parts of the  body that are made up of just 3letters (answers to follow)", user_id=freddie.id)
        keepgoing.save()
        keepgoing = PostModel(content="Owning a dog may reduce heart disease risk - says the American Heart Association", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="The body can produce enough heat in just half an hour to boil water. Each hour, the human body creates 350,000 joules of energy, which creates the same amount of energy as a 100-watt light bulb. This ends up being enough heat to boil a half gallon of water in just 30 minutes", user_id=freddie.id)
        keepgoing.save()
        keepgoing = PostModel(content="Getting more exercise may mean better sleep. Moderate exercise may increase the amount of deep sleep you get. While you won’t want to run a mile before bed if you want to be ready to sleep, getting some exercise earlier in the day may improve your overall bedtime experience.", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="My best mate Bob tried yoga for the first time, ending up tangled in the mat. He laughed it off, vowing to return.", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="I had a little gym mishap: mistaking the leg press for a rowing machine, I hilariously paddled my way to a workout", user_id=freddie.id)
        keepgoing.save()
        keepgoing = PostModel(content="My husband Tom's run turned into a race with a squirrel, sprinting through the park to the cheers of amused onlookers.", user_id=bertie.id)
        keepgoing.save()
        keepgoing = PostModel(content="My sister, Sarah's attempt at Zumba had her dancing out of sync, but her infectious laughter kept the class energized and entertained", user_id=bertie.id)
        keepgoing.save()

    # Session seeding..
        saturday = SessionModel(name="360degree Wake Up", date=date(2024, 4, 20), day="Saturday", capacity= 1, user_id=bertie.id)
        saturday.save()
        tuesday = SessionModel(name="Circuits", date=date(2024, 4, 23), day="Tuesday", capacity= 20, user_id=bertie.id)
        tuesday.save()
        saturday = SessionModel(name="360degree Wake Up", date=date(2024, 4, 27), day="Saturday", capacity= 20, user_id=bertie.id)
        saturday.save()
        tuesday = SessionModel(name="Circuits", date=date(2024, 4, 30), day="Tuesday", capacity= 20, user_id=bertie.id)
        tuesday.save()
        saturday = SessionModel(name="360degree Wake Up", date=date(2024, 5, 4), day="Saturday", capacity= 20, user_id=bertie.id)
        saturday.save()
        tuesday = SessionModel(name="Circuits", date=date(2024, 5, 7), day="Tuesday", capacity= 20, user_id=bertie.id)
        tuesday.save()
        saturday = SessionModel(name="360degree Wake Up", date=date(2024, 5, 11), day="Saturday", capacity= 20, user_id=bertie.id)
        saturday.save()
        tuesday = SessionModel(name="Circuits", date=date(2024, 5, 14), day="Tuesday", capacity= 20, user_id=bertie.id)
        saturday.save()

    # UserSession seeding..
        bertie_sat = UserSessionModel(user_id=bertie.id, session_id=saturday.id)
        bertie_sat.save()
        freddie_tue = UserSessionModel(user_id=freddie.id, session_id=tuesday.id)
        freddie_tue.save()
        betty_sat = UserSessionModel(user_id=betty.id, session_id=saturday.id)
        betty_sat.save()
        percy_tue = UserSessionModel(user_id=percy.id, session_id=tuesday.id)
        percy_tue.save()

    # PARQ seeding..
        bertie = ParqModel(question_one=True, question_two=True,question_three=True, question_four="This is a description", question_five="This is another description", question_six="And another description", question_seven=True, signed="This is a signature field", user_id=bertie.id)
        bertie.save()
        
    # Consent Form seeding..
        # bertie_consent = ConsentformModel(one=True, two=True, three=True, four=True, five=True, six=True, seven=True, eight=True, signed="This is a signature field", user_id=bertie.id)
        # bertie_consent.save()





        print("Database seeded!")
    except Exception as e:
        print(e)



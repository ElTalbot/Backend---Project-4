from app import app, db
from models.user import UserModel
from models.movement import MovementModel
from models.post import PostModel
from models.session import SessionModel
from datetime import datetime, date
from models.user_session import UserSessionModel

with app.app_context():

  try:
    print('Creating our database....')
    db.drop_all()
    db.create_all()

    print('Seeding the database!')

    # User seeding
    bertie = UserModel(username="bertie", email="bertiebert@bert.com", password="password", is_admin=True)
    bertie.save()

  #   # Movement seeding
    squatpulses = MovementModel(name="Squat Pulses", descriptionOne="1. From a standing position and your knees off lock - remember to keep your ears, shoulders and hip in line and your spine in neutral and brace your abdominals", descriptionTwo="2. From this position slowly lower into a squat position", descriptionThree="3. During the lowering movement make sure your heels remain flat and in contact withthe ground - this downward movement is about hinging at the hip and sticking your bottom out imagining you are about to sit onto the toilet.", descriptionFour="4. Stay in the squat position, gently pulse your legs in an up and down motion - make sure to maintain the tension in your thigh muscles throughout Be sure to keep the abdominals braced throughout", image="https://imgur.com/a/3nAPLnc", type="Strength", equipment="bodyweight", video="https://youtu.be/6VSTURgU0LQ", adaption="Slightly lowering into the squat and not lowering too deep will reduce the intensity of the exercise and allow for a gentler movement OR a Progression - The deeper the squat (the lower you go) the greater the intensity of the exercise - make sure to keep your feet flat on the floor and let this gauge how low you go", user_id=bertie.id)
    squatpulses.save()

    # Post seeding..
    keepgoing = PostModel(content="Find your way, and be who you are!!", user_id=bertie.id)
    keepgoing.save()

    # Session seeding..
    saturday = SessionModel(name="360degree Wake Up", date=date(2024, 4, 13), day="Saturday", capacity= 2, user_id=bertie.id)
    saturday.save()

    # UserSession seeding..
    bertie_sat = UserSessionModel(user_id=bertie.id, session_id=saturday.id)
    bertie_sat.save()


    print("Database seeded!")
  except Exception as e:
    print(e)



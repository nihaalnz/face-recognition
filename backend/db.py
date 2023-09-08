import asyncio
from prisma import Prisma
from prisma.models import User, Face
import detect


async def get_all_faces():
    return await Face.prisma().find_many(include={"user": True})


async def add_face_in_db(name: str, image_array) -> Face:
    user_det = await detect.check_face_in_db(image_array)
    if not isinstance(user_det, str):
        user = await User.prisma().create(
            data={
                "name": name,
            }
        )
        await Face.prisma().create(
            {"encoding": user_det.tolist(), "user": {"connect": {"id": user.id}}},
            include={"user": True},
        )

        return user
    return user_det


if __name__ == "__main__":

    async def main():
        prisma = Prisma(auto_register=True)
        await prisma.connect()

        # face = await get_all_faces()
        # print(face)

        # face = add_face("Ronnyda", [1.0, 2.0, 3.1, 60.5])
        # print(face)

        # face = verify_face([1, 5, 3.1, 4.5])
        # print(face)

    asyncio.run(main())

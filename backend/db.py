import asyncio
from prisma import Prisma
from prisma.models import User, Face
import detect

async def get_all_faces():
    return await Face.prisma().find_many(include={"user": True})


async def add_face(name: str) -> User:
    face_encoding = detect.get_face_encoding().tolist()
    user = await User.prisma().create(
        data={
            "name": name,
        }
    )
    face = await Face.prisma().create(
        {"encoding": face_encoding, "user": {"connect": {"id": user.id}}}, include={"user": True}
    )

    return face

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

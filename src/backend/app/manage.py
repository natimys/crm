import asyncio
import argparse
from sqlalchemy import select
from app.engine import async_session
from app.models import User, UserRole

async def make_admin(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Error, user with id {user_id} not found")
            return

        user.role = UserRole.ADMIN
        await session.commit()
        print(f"Success: User {user.login} (ID: {user_id}) is admin")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI to manage roles")
    subparsers = parser.add_subparsers(dest="command")

    admin_parser = subparsers.add_parser("set_admin")
    admin_parser.add_argument("--user-id", type=int, required=True, help="ID пользователя")

    args = parser.parse_args()

    if args.command == "set_admin":
        asyncio.run(make_admin(args.user_id))
    else:
        parser.print_help()

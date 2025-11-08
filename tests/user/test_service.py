import pytest

from mdabojbot.user.constants import UserGroup
from mdabojbot.user.models import User
from mdabojbot.user.service import get_random_admin, is_user_admin


@pytest.mark.asyncio
async def test_get_random_admin(db_session):
    admin_user = User(telegram_user_id=100, group=UserGroup.ADMIN)
    db_session.add(admin_user)
    await db_session.commit()

    retrieved_admin = await get_random_admin(session=db_session)
    assert retrieved_admin.telegram_user_id == 100

    admin_user2 = User(telegram_user_id=200, group=UserGroup.ADMIN)
    db_session.add(admin_user2)
    await db_session.commit()

    retrieved_admin2 = await get_random_admin(session=db_session)
    assert retrieved_admin2.telegram_user_id in [100, 200]

    await db_session.delete(admin_user)
    await db_session.delete(admin_user2)
    await db_session.commit()

    with pytest.raises(ValueError, match="There is not admin!"):
        await get_random_admin(session=db_session)


@pytest.mark.asyncio
async def test_is_user_admin(db_session):
    admin_user = User(telegram_user_id=100, group=UserGroup.ADMIN)
    regular_user = User(telegram_user_id=200, group=UserGroup.REGULAR)
    db_session.add(admin_user)
    db_session.add(regular_user)
    await db_session.commit()

    assert await is_user_admin(telegram_user_id=100, session=db_session)
    assert not await is_user_admin(telegram_user_id=200, session=db_session)

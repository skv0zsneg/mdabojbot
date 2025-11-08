import pytest
from sqlalchemy import select

from mdabojbot.prediction.models import Prediction
from mdabojbot.prediction.service import (
    create_prediction,
    get_random_prediction,
    get_unapproved_predictions,
    prediction_approve,
    prediction_delete,
)


@pytest.mark.asyncio
async def test_create_prediction(db_session):
    # Test creating a new prediction
    user_id = 123
    text = "Test prediction"
    prediction = await create_prediction(
        telegram_user_id=user_id, prediction_text=text, session=db_session
    )
    assert prediction.telegram_user_id == user_id
    assert prediction.text == text
    assert not prediction.is_approved

    # Verify it's in the database
    db_prediction = await db_session.get(Prediction, prediction.id)
    assert db_prediction is not None
    assert db_prediction.id == prediction.id


@pytest.mark.asyncio
async def test_get_unapproved_predictions(db_session):
    # Create a few predictions
    pred1 = Prediction(telegram_user_id=1, text="Unapproved 1", is_approved=False)
    pred2 = Prediction(telegram_user_id=2, text="Approved 2", is_approved=True)
    pred3 = Prediction(telegram_user_id=3, text="Unapproved 3", is_approved=False)
    db_session.add_all([pred1, pred2, pred3])
    await db_session.commit()

    unapproved = await get_unapproved_predictions(session=db_session)
    assert len(unapproved) == 2
    assert unapproved[0].id in [pred1.id, pred3.id]
    assert unapproved[1].id in [pred1.id, pred3.id]
    assert unapproved[0].id != unapproved[1].id


@pytest.mark.asyncio
async def test_prediction_delete(db_session):
    # Create a prediction to delete
    pred = Prediction(telegram_user_id=1, text="To delete", is_approved=False)
    db_session.add(pred)
    await db_session.commit()

    # Delete it
    await prediction_delete(prediction_id=pred.id, session=db_session)

    # Verify it's gone
    db_pred = await db_session.get(Prediction, pred.id)
    assert db_pred is None

    # Verify it raises error if not found
    with pytest.raises(ValueError, match="There is no prediction with id=999!"):
        await prediction_delete(prediction_id=999, session=db_session)


@pytest.mark.asyncio
async def test_get_random_prediction_no_approved(db_session):
    # Ensure no approved predictions exist
    await db_session.execute(select(Prediction).where(Prediction.is_approved))
    result = await db_session.execute(select(Prediction))
    all_preds = result.scalars().all()
    for p in all_preds:
        p.is_approved = False
    await db_session.commit()

    # Should raise ValueError
    with pytest.raises(ValueError, match="There is no approved prediction!"):
        await get_random_prediction(session=db_session)


@pytest.mark.asyncio
async def test_prediction_approve(db_session):
    # Create an unapproved prediction
    pred = Prediction(telegram_user_id=1, text="To approve", is_approved=False)
    db_session.add(pred)
    await db_session.commit()

    # Approve it
    approved_pred = await prediction_approve(prediction_id=pred.id, session=db_session)
    assert approved_pred.id == pred.id
    assert approved_pred.is_approved

    # Verify in DB
    db_pred = await db_session.get(Prediction, pred.id)
    assert db_pred.is_approved

    # Verify error if not found
    with pytest.raises(ValueError, match="There is no prediction with id=999!"):
        await prediction_approve(prediction_id=999, session=db_session)

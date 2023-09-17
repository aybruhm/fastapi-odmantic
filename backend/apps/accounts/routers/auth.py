# Stdlib Imports
import json

# FastAPI Imports
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Own Imports
from apps.accounts.dto.users_dto import (
    UserCreateDTO,
    UserLoginDTO,
    UserAccountRecoverDTO,
    UserAccountRecoverConfirmDTO,
    UserAccountRecoverCompleteDTO,
)
from apps.accounts.manager.db_manager import setup_user_account
from apps.accounts.manager.service_manager import (
    login_user_account,
    recover_user_account,
    resend_otp_code,
    verify_otp_code,
    complete_recover_account,
)


# initialize api router
router = APIRouter(tags=["Users (auth)"], prefix="/users")


@router.post("/register/")
async def create_account(payload: UserCreateDTO) -> JSONResponse:
    """API Router responsible for creating a new user account.

    Args:
       payload (UserCreateDTO): required payload

    Returns:
        data: the newly created user account
    """

    ngo_account = await setup_user_account(payload)
    return JSONResponse(
        content={
            "message": "Account created successfully",
            "data": json.loads(ngo_account.json()),
        }
    )


@router.post("/login/")
async def login_account(payload: UserLoginDTO) -> JSONResponse:
    """API Router responsible for signing in a user account.

    Args:
       payload (UserLoginDTO): required payload

    Returns:
        data: user account data and jwt token
    """

    jwt_token = await login_user_account(payload.email, payload.password)
    return JSONResponse(content={"token": jwt_token})


@router.post("/recover/")
async def recover_account(payload: UserAccountRecoverDTO) -> JSONResponse:
    """API Router responsible for recovering a user account.

    Args:
       payload (UserAccountRecoverDTO): required payload

    Returns:
        data: confirmation message
    """

    await recover_user_account(payload.email)
    return JSONResponse(
        content={
            "message": "Account recovery initiated. Kindly check your email for otp code.",
        }
    )


@router.post("/recover/resend-otp/")
async def recover_account_resend_otp(
    payload: UserAccountRecoverDTO,
) -> JSONResponse:
    """API Router responsible for resending a user account password recovery otp.

    Args:
       payload (UserAccountRecoverDTO): required payload

    Returns:
        data: confirmation message
    """

    otp_resent = await resend_otp_code(payload.email)
    if otp_resent:
        return JSONResponse({"message": "OTP successfully resent!"})
    return JSONResponse(
        {"detail": {"message": "OTP resend failed. Please try again."}},
        status_code=400,
    )


@router.post("/recover/verify-otp/")
async def recover_account_verify_otp(
    payload: UserAccountRecoverConfirmDTO,
) -> JSONResponse:
    """API Router responsible for verifying a user account password recovery otp.

    Args:
       payload (UserAccountRecoverConfirmDTO): required payload

    Returns:
        data: confirmation message
    """

    otp_verified = await verify_otp_code(payload.email, payload.otp_code)
    if otp_verified:
        return JSONResponse({"message": "OTP verified!"})
    return JSONResponse(
        {"detail": {"message": "OTP verification failed. Please try again."}},
        status_code=400,
    )


@router.post("/recover/complete/")
async def recover_account_complete(
    payload: UserAccountRecoverCompleteDTO,
) -> JSONResponse:
    """API Router responsible for completing a user account password recovery.

    Args:
       payload (UserAccountRecoverCompleteDTO): required payload

    Returns:
        data: confirmation message
    """

    await complete_recover_account(payload.email, payload.password)
    return JSONResponse(
        {"message": "Account recovery successfully completed!"}
    )

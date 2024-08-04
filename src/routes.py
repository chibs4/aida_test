from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse
from tortoise.exceptions import IntegrityError
from pydantic import AnyHttpUrl, constr

from model import LinkRealation
from utils import generate_random_link
import errors
from settings import settings

router = APIRouter()


@router.post(
    "/api/generate_short_url",
)
async def create_link(long_url: AnyHttpUrl):
    if await LinkRealation.filter(original_link=long_url).exists():
        raise errors.link_already_exists(long_url)
    # Пробуем сгенерировать ссылку несколько раз, потому что она может быть уже в базе
    for _ in range(10):
        new_link = generate_random_link()
        try:
            new_model = await LinkRealation.create(
                original_link=long_url, new_link=new_link
            )
            full_link = f"http://localhost:{settings.SERVER_PORT}/{new_model.new_link}"
            return full_link
        except IntegrityError:
            continue
    raise errors.failed_to_generate()


@router.get("/api/count/{short_link}")
async def get_link_redirect_count(short_link=constr(max_length=5)):
    redirect = await LinkRealation.get_or_none(new_link=short_link)
    if not redirect:
        raise errors.link_not_found(short_link)
    return redirect.redirect_count


@router.get("/{short_link}")
async def redirect(request: Request):
    rel_url = request.url.path.lstrip("/")
    if len(rel_url) > 5:
        raise errors.link_too_long()
    redirect = await LinkRealation.get_or_none(new_link=rel_url)
    if not redirect:
        raise errors.link_not_found(rel_url)
    await redirect.increase_redirect_count()
    return RedirectResponse(redirect.original_link, status_code=301)

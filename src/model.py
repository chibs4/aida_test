from tortoise import Tortoise
from tortoise import fields, models


class LinkRealation(models.Model):
    id = fields.IntField(pk=True)
    original_link = fields.CharField(max_length=300, unique=True, index=True)
    new_link = fields.CharField(max_length=5, unique=True, index=True)
    redirect_count = fields.IntField(default=0)

    async def increase_redirect_count(self):
        self.redirect_count += 1
        await self.save()

    class Meta:
        table = "link_relation"


Tortoise.init_models(["model"], "model")

import discord

class MemberResource:
    def __init__(self, ctx, member):
        self.ctx = ctx
        self.member = member

        self._get_member()
        if self.member is None:
            try:
                self.member = discord.utils.get(self.ctx.guild.members, id=int(self.ctx.channel.topic[9:]))
                if self.member is None:
                    self.member = self.ctx.author
            except (ValueError, TypeError):
                self.member = self.ctx.author

    def _get_member(self):
        """Fetch a member by its name or nickname."""

        if isinstance(self.member, discord.Member):
            return

        if self.member is None:
            self.member = None
            return

        for m in self.ctx.guild.members:
            if m.display_name.lower().startswith(self.member.lower()):
                self.member = m
                return

            if m.name.lower().startswith(self.member.lower()):
                self.member = m
                return

        self.member = None

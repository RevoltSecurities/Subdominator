from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from subdominator.modules.models.models import Subdomain

async def get_domain(db: AsyncSession, domain: str):
    result = await db.execute(select(Subdomain).filter(Subdomain.domain == domain))
    return result.scalars().first()

async def add_or_update_domain(db: AsyncSession, domain: str, subdomains: set):
    existing_entry = await get_domain(db, domain)
    if existing_entry:
        existing_subdomains = set(existing_entry.subdomains.split(",")) if existing_entry.subdomains else set()
        new_subdomains = existing_subdomains.union(subdomains)
        existing_entry.subdomains = ",".join(sorted(new_subdomains))
    else:
        new_entry = Subdomain(domain=domain, subdomains=",".join(sorted(subdomains)))
        db.add(new_entry)
    await db.commit()

async def get_all_domains(db: AsyncSession):
    result = await db.execute(select(Subdomain))
    return result.scalars().all()

async def get_subdomains(db: AsyncSession, domain: str):
    domain_entry = await get_domain(db, domain)
    return set(domain_entry.subdomains.split(",")) if domain_entry and domain_entry.subdomains else set()

async def delete_domain(db: AsyncSession, domain: str):
    domain_entry = await get_domain(db, domain)
    if domain_entry:
        await db.delete(domain_entry)
        await db.commit()
        return True
    return False


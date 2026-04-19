from __future__ import annotations

from collections.abc import Iterable

from subdominator.core.provider_config import ProviderConfig
from subdominator.http.retryable import RetryableHttpClient
from subdominator.resources.base import BaseResource
from subdominator.resources.catalog import RESOURCE_CATALOG
from subdominator.resources.providers.abuseipdb import AbuseIpDbResource
from subdominator.resources.providers.alienvault import AlienVaultResource
from subdominator.resources.providers.anubis import AnubisResource
from subdominator.resources.providers.argosdns import ArgosDnsResource
from subdominator.resources.providers.arpsyndicate import ArpSyndicateResource
from subdominator.resources.providers.binaryedge import BinaryEdgeResource
from subdominator.resources.providers.bevigil import BeVigilResource
from subdominator.resources.providers.bufferover import BufferOverResource
from subdominator.resources.providers.builtwith import BuiltWithResource
from subdominator.resources.providers.c99 import C99Resource
from subdominator.resources.providers.censys import CensysResource
from subdominator.resources.providers.certspotter import CertSpotterResource
from subdominator.resources.providers.chaos import ChaosResource
from subdominator.resources.providers.chinaz import ChinazResource
from subdominator.resources.providers.coderog import CodeRogResource
from subdominator.resources.providers.commoncrawl import CommonCrawlResource
from subdominator.resources.providers.crtsh import CrtShResource
from subdominator.resources.providers.cyfare import CyfareResource
from subdominator.resources.providers.digitalyama import DigitalYamaResource
from subdominator.resources.providers.digitorus import DigitorusResource
from subdominator.resources.providers.dnsdb import DnsdbResource
from subdominator.resources.providers.dnsdumpster import DnsDumpsterResource
from subdominator.resources.providers.dnsrepo import DnsRepoResource
from subdominator.resources.providers.domainsproject import DomainsProjectResource
from subdominator.resources.providers.driftnet import DriftnetResource
from subdominator.resources.providers.fofa import FofaResource
from subdominator.resources.providers.facebook import FacebookResource
from subdominator.resources.providers.fullhunt import FullHuntResource
from subdominator.resources.providers.github import GithubResource
from subdominator.resources.providers.google import GoogleResource
from subdominator.resources.providers.hackertarget import HackerTargetResource
from subdominator.resources.providers.huntermap import HunterMapResource
from subdominator.resources.providers.hudsonrock import HudsonRockResource
from subdominator.resources.providers.intelx import IntelXResource
from subdominator.resources.providers.leakix import LeakIXResource
from subdominator.resources.providers.merklemap import MerkleMapResource
from subdominator.resources.providers.myssl import MySslResource
from subdominator.resources.providers.netlas import NetlasResource
from subdominator.resources.providers.odin import OdinResource
from subdominator.resources.providers.onyphe import OnypheResource
from subdominator.resources.providers.profundis import ProfundisResource
from subdominator.resources.providers.pugrecon import PugreconResource
from subdominator.resources.providers.quake import QuakeResource
from subdominator.resources.providers.racent import RacentResource
from subdominator.resources.providers.rapidapi import RapidApiResource
from subdominator.resources.providers.rapidfinder import RapidFinderResource
from subdominator.resources.providers.rapidscan import RapidScanResource
from subdominator.resources.providers.rapiddns import RapidDnsResource
from subdominator.resources.providers.reconcloud import ReconCloudResource
from subdominator.resources.providers.reconeer import ReconeerResource
from subdominator.resources.providers.redhuntlabs import RedHuntLabsResource
from subdominator.resources.providers.riddler import RiddlerResource
from subdominator.resources.providers.robtex import RobtexResource
from subdominator.resources.providers.rsecloud import RseCloudResource
from subdominator.resources.providers.securitytrails import SecurityTrailsResource
from subdominator.resources.providers.shodan import ShodanResource
from subdominator.resources.providers.shodanx import ShodanXResource
from subdominator.resources.providers.shrewdeye import ShrewdEyeResource
from subdominator.resources.providers.sitedossier import SiteDossierResource
from subdominator.resources.providers.submd import SubMdResource
from subdominator.resources.providers.thc import ThcResource
from subdominator.resources.providers.threatbook import ThreatBookResource
from subdominator.resources.providers.threatcrowd import ThreatCrowdResource
from subdominator.resources.providers.threatminer import ThreatMinerResource
from subdominator.resources.providers.trickest import TrickestResource
from subdominator.resources.providers.urlscan import UrlscanResource
from subdominator.resources.providers.virustotal import VirusTotalResource
from subdominator.resources.providers.waybackarchive import WaybackArchiveResource
from subdominator.resources.providers.windvane import WindvaneResource
from subdominator.resources.providers.whoisfreaks import WhoisFreaksResource
from subdominator.resources.providers.whoisxml import WhoisXmlResource
from subdominator.resources.providers.zoomeyeapi import ZoomEyeApiResource


RESOURCE_TYPES = [
    AbuseIpDbResource,
    AlienVaultResource,
    AnubisResource,
    ArgosDnsResource,
    ArpSyndicateResource,
    BinaryEdgeResource,
    BeVigilResource,
    BufferOverResource,
    BuiltWithResource,
    C99Resource,
    CensysResource,
    CertSpotterResource,
    ChaosResource,
    ChinazResource,
    CodeRogResource,
    CommonCrawlResource,
    CrtShResource,
    CyfareResource,
    DigitalYamaResource,
    DigitorusResource,
    DnsdbResource,
    DnsDumpsterResource,
    DnsRepoResource,
    DomainsProjectResource,
    DriftnetResource,
    FacebookResource,
    FofaResource,
    FullHuntResource,
    GithubResource,
    GoogleResource,
    HackerTargetResource,
    HunterMapResource,
    HudsonRockResource,
    IntelXResource,
    LeakIXResource,
    MerkleMapResource,
    MySslResource,
    NetlasResource,
    OdinResource,
    OnypheResource,
    ProfundisResource,
    PugreconResource,
    QuakeResource,
    RacentResource,
    RapidApiResource,
    RapidFinderResource,
    RapidScanResource,
    RapidDnsResource,
    ReconCloudResource,
    ReconeerResource,
    RedHuntLabsResource,
    RiddlerResource,
    RobtexResource,
    RseCloudResource,
    SecurityTrailsResource,
    ShodanResource,
    ShodanXResource,
    ShrewdEyeResource,
    SiteDossierResource,
    SubMdResource,
    ThcResource,
    ThreatBookResource,
    ThreatCrowdResource,
    ThreatMinerResource,
    TrickestResource,
    UrlscanResource,
    VirusTotalResource,
    WaybackArchiveResource,
    WindvaneResource,
    WhoisFreaksResource,
    WhoisXmlResource,
    ZoomEyeApiResource,
]

DEFAULT_DISABLED_RESOURCES = {
    "commoncrawl",
    "github",
    "virustotal",
    "waybackarchive",
}


class ResourceRegistry:
    def __init__(
        self,
        client: RetryableHttpClient,
        provider_config: ProviderConfig,
        dork: str | None = None,
    ) -> None:
        self._client = client
        self._provider_config = provider_config
        self._resources = {}
        for resource_type in RESOURCE_TYPES:
            if resource_type.__name__ == "GoogleResource":
                self._resources[resource_type.name] = resource_type(client, provider_config, dork=dork)
            else:
                self._resources[resource_type.name] = resource_type(client, provider_config)

    def all_names(self) -> list[str]:
        return sorted(self._resources)

    def all_metadata(self) -> list[dict[str, str | bool]]:
        return sorted(
            [
                {
                    "name": name,
                    "label": RESOURCE_CATALOG.get(name, {}).get("label", name),
                    "url": RESOURCE_CATALOG.get(name, {}).get("url", ""),
                    "requires_config": resource.requires_config,
                    "has_optional_config": getattr(resource, "has_optional_config", False),
                }
                for name, resource in self._resources.items()
            ],
            key=lambda item: str(item["name"]),
        )

    def select(
        self,
        include: Iterable[str] | None = None,
        exclude: Iterable[str] | None = None,
        include_all: bool = False,
    ) -> list[BaseResource]:
        include_set = {item.strip().lower() for item in include or [] if item.strip()}
        exclude_set = {item.strip().lower() for item in exclude or [] if item.strip()}

        if include_set:
            names = include_set.intersection(self._resources)
        elif include_all:
            names = set(self._resources)
        else:
            names = set(self._resources) - DEFAULT_DISABLED_RESOURCES

        names -= exclude_set
        return [self._resources[name] for name in sorted(names)]

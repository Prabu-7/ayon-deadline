from pydantic import validator

from ayon_server.settings import (
    BaseSettingsModel,
    SettingsField,
    ensure_unique_names,
    task_types_enum,
)


class LimitGroupsSubmodel(BaseSettingsModel):
    _layout = "expanded"
    name: str = SettingsField(title="Name")
    value: list[str] = SettingsField(
        default_factory=list,
        title="Limit Groups"
    )


class EnvSearchReplaceSubmodel(BaseSettingsModel):
    _layout = "compact"
    name: str = SettingsField(title="Name")
    value: str = SettingsField(title="Value")


class CollectAYONServerToFarmJobModel(BaseSettingsModel):
    enabled: bool = SettingsField(False, title="Enabled")


def extract_jobinfo_overrides_enum():
    """Enum of fields that could be overridden by artist in Publisher UI"""
    return [
        {"label": "Department", "value": "department"},
        {"label": "Delay job (timecode dd:hh:mm:ss)", "value": "job_delay"},
        {"label": "Frames per Task", "value": "chunk_size"},
        {"label": "Group", "value": "group"},
        {"label": "Priority", "value": "priority"},
        {"label": "Limit groups", "value": "limit_groups"},
        {"label": "Primary pool", "value": "primary_pool"},
        {"label": "Secondary pool", "value": "secondary_pool"},
        {"label": "Machine List", "value": "machine_list"},
        {"label": "Machine List is a Deny", "value": "machine_list_deny"},
    ]


class CollectJobInfoItem(BaseSettingsModel):
    _layout = "expanded"
    host_names: list[str] = SettingsField(
        default_factory=list,
        title="Host names"
    )
    task_types: list[str] = SettingsField(
        default_factory=list,
        title="Task types",
        enum_resolver=task_types_enum
    )
    task_names: list[str] = SettingsField(
        default_factory=list,
        title="Task names"
    )

    #########################################

    chunk_size: int = SettingsField(999, title="Frames per Task")
    priority: int = SettingsField(50, title="Priority")
    group: str = SettingsField("", title="Group")
    limit_groups: list[str] = SettingsField(
        default_factory=list,
        title="Limit Groups"
    )
    primary_pool: str = SettingsField("", title="Primary Pool")
    secondary_pool: str = SettingsField("", title="Secondary Pool")
    machine_limit: int = SettingsField(
        0,
        title="Machine Limit",
        description=(
            "Specifies the maximum number of machines this job can be"
            " rendered on at the same time (default = 0, which means"
            " unlimited)."
        )
    )
    machine_list: list[str] = SettingsField(
        default_factory=list,
        title="Machine List",
        description=(
            "List of workers where submission can/cannot run "
            "based on Machine Allow/Deny toggle."
        )
    )
    machine_list_deny: bool = SettingsField(
        False, title="Machine List is a Deny",
        description=(
            "Explicitly DENY list of machines to render. Without it "
            "it will ONLY ALLOW machines from list."
        )
    )
    concurrent_tasks: int = SettingsField(
        1, title="Number of concurrent tasks")
    department: str = SettingsField("", title="Department")
    use_gpu: bool = SettingsField("", title="Use GPU")
    job_delay: str = SettingsField(
        "", title="Delay job",
        placeholder="dd:hh:mm:ss"
    )
    use_published: bool = SettingsField(True, title="Use Published scene")
    use_asset_dependencies: bool = SettingsField(
        True, title="Use Asset dependencies")
    use_workfile_dependency: bool = SettingsField(
        True, title="Workfile Dependency")
    multiprocess: bool = SettingsField(False, title="Multiprocess")

    env_allowed_keys: list[str] = SettingsField(
        default_factory=list,
        title="Allowed environment keys",
        description="Pass selected environment variables with current value"
    )
    env_search_replace_values: list[EnvSearchReplaceSubmodel] = SettingsField(
        default_factory=list,
        title="Search & replace in environment values",
        description="Replace string values in 'Name' with value from 'Value'"
    )
    additional_job_info: str = SettingsField(
        "",
        title="Additional JobInfo data",
        widget="textarea",
        description=
            "Dictionary (JSON parsable) to paste unto JobInfo of submission"
    )
    additional_plugin_info: str = SettingsField(
        "",
        title="Additional PluginInfo data",
        widget="textarea",
        description=
            "Dictionary (JSON parsable) to paste unto PluginInfo "
            "of submission"
    )
    overrides: list[str] = SettingsField(
        "",
        enum_resolver=extract_jobinfo_overrides_enum,
        title="Exposed Overrides",
        description=(
            "Expose the attribute in this list to the user when publishing."
        )
    )


class CollectJobInfoModel(BaseSettingsModel):
    _isGroup = True
    enabled: bool = SettingsField(False)
    profiles: list[CollectJobInfoItem] = SettingsField(default_factory=list)


class ValidateExpectedFilesModel(BaseSettingsModel):
    enabled: bool = SettingsField(True, title="Enabled")
    active: bool = SettingsField(True, title="Active")
    allow_user_override: bool = SettingsField(
        True, title="Allow user change frame range"
    )
    families: list[str] = SettingsField(
        default_factory=list, title="Trigger on families"
    )
    targets: list[str] = SettingsField(
        default_factory=list, title="Trigger for plugins"
    )


def tile_assembler_enum():
    """Return a list of value/label dicts for the enumerator.

    Returning a list of dicts is used to allow for a custom label to be
    displayed in the UI.
    """
    return [
        {
            "value": "DraftTileAssembler",
            "label": "Draft Tile Assembler"
        }
    ]


class ScenePatchesSubmodel(BaseSettingsModel):
    _layout = "expanded"
    name: str = SettingsField(title="Patch name")
    regex: str = SettingsField(title="Patch regex")
    line: str = SettingsField(title="Patch line")


class MayaSubmitDeadlineModel(BaseSettingsModel):
    """Maya deadline submitter settings."""

    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")
    import_reference: bool = SettingsField(
        title="Use Scene with Imported Reference"
    )
    tile_priority: int = SettingsField(title="Tile Priority")

    tile_assembler_plugin: str = SettingsField(
        title="Tile Assembler Plugin",
        enum_resolver=tile_assembler_enum,
    )

    scene_patches: list[ScenePatchesSubmodel] = SettingsField(
        default_factory=list,
        title="Scene patches",
    )
    strict_error_checking: bool = SettingsField(
        title="Disable Strict Error Check profiles"
    )

    @validator("scene_patches")
    def validate_unique_names(cls, value):
        ensure_unique_names(value)
        return value


class MaxSubmitDeadlineModel(BaseSettingsModel):
    enabled: bool = SettingsField(True)
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


def fusion_deadline_plugin_enum():
    """Return a list of value/label dicts for the enumerator.

    Returning a list of dicts is used to allow for a custom label to be
    displayed in the UI.
    """
    return [
        {
            "value": "Fusion",
            "label": "Fusion"
        },
        {
            "value": "FusionCmd",
            "label": "FusionCmd"
        }
    ]


class FusionSubmitDeadlineModel(BaseSettingsModel):
    enabled: bool = SettingsField(True, title="Enabled")
    optional: bool = SettingsField(False, title="Optional")
    active: bool = SettingsField(True, title="Active")
    concurrent_tasks: int = SettingsField(
        1, title="Number of concurrent tasks"
    )
    plugin: str = SettingsField("Fusion",
                                enum_resolver=fusion_deadline_plugin_enum,
                                title="Deadline Plugin")


class NukeSubmitDeadlineModel(BaseSettingsModel):
    """Nuke deadline submitter settings."""

    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")

    node_class_limit_groups: list[LimitGroupsSubmodel] = SettingsField(
        default_factory=list,
        title="Node based Limit Groups",
    )


class HarmonySubmitDeadlineModel(BaseSettingsModel):
    """Harmony deadline submitter settings."""

    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


class HoudiniSubmitDeadlineModel(BaseSettingsModel):
    """Houdini deadline render submitter settings."""
    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")

    export_priority: int = SettingsField(title="Export Priority")
    export_chunk_size: int = SettingsField(title="Export Chunk Size")
    export_group: str = SettingsField(title="Export Group")
    export_limits: str = SettingsField(
        title="Export Limit Groups",
        description=(
            "Enter a comma separated list of limits.\n"
            "Specifies the limit groups that this job is a member of (default = blank)."
        )
    )
    export_machine_limit: int = SettingsField(
        title="Export Machine Limit",
        description=(
            "Specifies the maximum number of machines this job can be"
            " rendered on at the same time (default = 0, which means"
            " unlimited)."
        )
    )


class HoudiniCacheSubmitDeadlineModel(BaseSettingsModel):
    """Houdini deadline cache submitter settings."""
    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


class AfterEffectsSubmitDeadlineModel(BaseSettingsModel):
    """After Effects deadline submitter settings."""

    enabled: bool = SettingsField(title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


class CelactionSubmitDeadlineModel(BaseSettingsModel):
    enabled: bool = SettingsField(True, title="Enabled")
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


class BlenderSubmitDeadlineModel(BaseSettingsModel):
    enabled: bool = SettingsField(True)
    optional: bool = SettingsField(title="Optional")
    active: bool = SettingsField(title="Active")


class AOVFilterSubmodel(BaseSettingsModel):
    _layout = "expanded"
    name: str = SettingsField(title="Host")
    value: list[str] = SettingsField(
        default_factory=list,
        title="AOV regex"
    )


class ProcessCacheJobFarmModel(BaseSettingsModel):
    """Process submitted job on farm."""

    enabled: bool = SettingsField(title="Enabled")
    deadline_department: str = SettingsField(title="Department")
    deadline_pool: str = SettingsField(title="Pool")
    deadline_group: str = SettingsField(title="Group")
    deadline_priority: int = SettingsField(title="Priority")


class ProcessSubmittedJobOnFarmModel(BaseSettingsModel):
    """Process submitted job on farm."""

    enabled: bool = SettingsField(title="Enabled")
    deadline_department: str = SettingsField(title="Department")
    deadline_pool: str = SettingsField(title="Pool")
    deadline_group: str = SettingsField(title="Group")
    deadline_priority: int = SettingsField(title="Priority")
    skip_integration_repre_list: list[str] = SettingsField(
        default_factory=list,
        title="Skip integration of representation with ext"
    )
    families_transfer: list[str] = SettingsField(
        default_factory=list,
        title=(
            "List of family names to transfer\n"
            "to generated instances (AOVs for example)."
        )
    )
    aov_filter: list[AOVFilterSubmodel] = SettingsField(
        default_factory=list,
        title="Reviewable products filter",
    )

    @validator("aov_filter")
    def validate_unique_names(cls, value):
        ensure_unique_names(value)
        return value


class PublishPluginsModel(BaseSettingsModel):
    CollectJobInfo: CollectJobInfoModel = SettingsField(
        default_factory=CollectJobInfoModel,
        title="Collect JobInfo")
    CollectAYONServerToFarmJob: CollectAYONServerToFarmJobModel = SettingsField(  # noqa
        default_factory=CollectAYONServerToFarmJobModel,
        title="Add AYON server to farm job",
        description=(
            "When enabled submit along your `AYON_SERVER_URL` to the farm job."
            " On the Deadline AYON Plug-in on the Deadline Repository settings"
            " you can specify a custom API key for those server URLs."
        )
    )
    ValidateExpectedFiles: ValidateExpectedFilesModel = SettingsField(
        default_factory=ValidateExpectedFilesModel,
        title="Validate Expected Files"
    )
    AfterEffectsSubmitDeadline: AfterEffectsSubmitDeadlineModel = (
        SettingsField(
            default_factory=AfterEffectsSubmitDeadlineModel,
            title="After Effects to deadline",
            section="Hosts"
        )
    )
    BlenderSubmitDeadline: BlenderSubmitDeadlineModel = SettingsField(
        default_factory=BlenderSubmitDeadlineModel,
        title="Blender Submit Deadline")
    CelactionSubmitDeadline: CelactionSubmitDeadlineModel = SettingsField(
        default_factory=CelactionSubmitDeadlineModel,
        title="Celaction Submit Deadline")
    FusionSubmitDeadline: FusionSubmitDeadlineModel = SettingsField(
        default_factory=FusionSubmitDeadlineModel,
        title="Fusion submit to Deadline")
    HarmonySubmitDeadline: HarmonySubmitDeadlineModel = SettingsField(
        default_factory=HarmonySubmitDeadlineModel,
        title="Harmony Submit to deadline")
    HoudiniCacheSubmitDeadline: HoudiniCacheSubmitDeadlineModel = SettingsField(
        default_factory=HoudiniCacheSubmitDeadlineModel,
        title="Houdini Submit cache to deadline")
    HoudiniSubmitDeadline: HoudiniSubmitDeadlineModel = SettingsField(
        default_factory=HoudiniSubmitDeadlineModel,
        title="Houdini Submit render to deadline")
    MaxSubmitDeadline: MaxSubmitDeadlineModel = SettingsField(
        default_factory=MaxSubmitDeadlineModel,
        title="Max Submit to deadline")
    MayaSubmitDeadline: MayaSubmitDeadlineModel = SettingsField(
        default_factory=MayaSubmitDeadlineModel,
        title="Maya Submit to deadline")
    NukeSubmitDeadline: NukeSubmitDeadlineModel = SettingsField(
        default_factory=NukeSubmitDeadlineModel,
        title="Nuke Submit to deadline")
    ProcessSubmittedCacheJobOnFarm: ProcessCacheJobFarmModel = SettingsField(
        default_factory=ProcessCacheJobFarmModel,
        title="Process submitted cache Job on farm",
        section="Publish Jobs")
    ProcessSubmittedJobOnFarm: ProcessSubmittedJobOnFarmModel = SettingsField(
        default_factory=ProcessSubmittedJobOnFarmModel,
        title="Process submitted job on farm")


DEFAULT_DEADLINE_PLUGINS_SETTINGS = {
    "CollectDeadlinePools": {
        "primary_pool": "",
        "secondary_pool": ""
    },
    "CollectAYONServerToFarmJob": {
        "enabled": False
    },
    "ValidateExpectedFiles": {
        "enabled": True,
        "active": True,
        "allow_user_override": True,
        "families": [
            "render"
        ],
        "targets": [
            "deadline"
        ]
    },
    "AfterEffectsSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "BlenderSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "CelactionSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "FusionSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "HarmonySubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "HoudiniCacheSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "HoudiniSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
        "export_priority": 50,
        "export_chunk_size": 10,
        "export_group": "",
        "export_limits": "",
        "export_machine_limit": 0
    },
    "MaxSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "MayaSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
        "tile_assembler_plugin": "DraftTileAssembler",
        "import_reference": False,
        "strict_error_checking": True,
        "tile_priority": 50,
        "scene_patches": []
    },
    "NukeSubmitDeadline": {
        "enabled": True,
        "optional": False,
        "active": True,
    },
    "ProcessSubmittedCacheJobOnFarm": {
        "enabled": True,
        "deadline_department": "",
        "deadline_pool": "",
        "deadline_group": "",
        "deadline_priority": 50
    },
    "ProcessSubmittedJobOnFarm": {
        "enabled": True,
        "deadline_department": "",
        "deadline_pool": "",
        "deadline_group": "",
        "deadline_priority": 50,
        "skip_integration_repre_list": [],
        "families_transfer": ["render3d", "render2d", "slate"],
        "aov_filter": [
            {
                "name": "maya",
                "value": [
                    ".*([Bb]eauty).*"
                ]
            },
            {
                "name": "blender",
                "value": [
                    ".*([Bb]eauty).*"
                ]
            },
            {
                "name": "aftereffects",
                "value": [
                    ".*"
                ]
            },
            {
                "name": "celaction",
                "value": [
                    ".*"
                ]
            },
            {
                "name": "harmony",
                "value": [
                    ".*"
                ]
            },
            {
                "name": "max",
                "value": [
                    ".*"
                ]
            },
            {
                "name": "fusion",
                "value": [
                    ".*"
                ]
            }
        ]
    }
}

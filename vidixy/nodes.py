from __future__ import annotations

import sys
import importlib
import inspect
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    NamedTuple,
    ParamSpec,
    TypeVar,
)
from pathlib import Path

T = TypeVar("T")
P = ParamSpec("P")


class VidixyNode(Generic[P, T]):
    """Vidixy node."""

    name: str
    description: str
    category: str
    func: Callable[P, T]
    inputs: list[NodeInput]
    outputs: list[NodeOutput]
    controls: list[NodeControl]

    def __init__(
        self,
        name: str,
        description: str,
        category: str,
        func: Callable[P, T],
        inputs: list[NodeInput],
        controls: list[NodeControl],
        outputs: list[NodeOutput],
    ):
        self.name = name
        self.description = description
        self.category = category
        self.func = func
        self.inputs = inputs
        self.controls = controls
        self.outputs = outputs

    def __repr__(self):
        return (
            f"<VidixyNode {self.name} inputs={self.inputs} "
            f"controls={self.controls} outputs={self.outputs}>"
        )

    sockets: ClassVar[set[str]] = set()
    nodes: ClassVar[list[VidixyNode[..., Any]]] = []


class NodeInput(NamedTuple):
    name: str
    socket: str
    description: str


class NodeOutput(NamedTuple):
    name: str
    socket: str
    description: str


class NodeControl(NamedTuple):
    name: str
    type: str
    default: Any
    description: str


def node(name: str | None = None, description: str = "", category: str = "General"):
    """Create a node."""

    def wrapper(builder: VidixyNodeBuilder[P, T]) -> Callable[P, T]:
        node = VidixyNode(
            name=name or normalize_name(builder.func.__name__),
            description=description,
            category=category,
            func=builder.func,
            inputs=builder.inputs,
            controls=builder.controls,
            outputs=builder.outputs,
        )
        VidixyNode.sockets.update(input.socket for input in node.inputs)
        VidixyNode.sockets.update(output.socket for output in node.outputs)
        VidixyNode.nodes.append(node)

        return builder.func

    return wrapper


class VidixyNodeBuilder(Generic[P, T]):
    func: Callable[P, T]
    annotations: list[tuple[str, Any]]
    inputs: list[NodeInput]
    controls: list[NodeControl]
    outputs: list[NodeOutput]

    def __init__(self, func: Callable[P, T]):
        self.func = func
        self.annotations = list(inspect.get_annotations(self.func).items())
        self.inputs = []
        self.controls = []
        self.outputs = []


def input(name: str, socket: str | None = None, description: str = ""):
    """Add an input to a node."""

    def wrapper(
        func: Callable[P, T] | VidixyNodeBuilder[P, T]
    ) -> VidixyNodeBuilder[P, T]:
        if not isinstance(func, VidixyNodeBuilder):
            func = VidixyNodeBuilder(func)

        _, annotation = func.annotations.pop()
        func.inputs.append(
            NodeInput(
                name=name, socket=socket or annotation.__name__, description=description
            )
        )

        return func

    return wrapper


def control(name: str, description: str = "", default: Any = None):
    """Add a control to a node."""

    def wrapper(
        func: Callable[P, T] | VidixyNodeBuilder[P, T]
    ) -> VidixyNodeBuilder[P, T]:
        if not isinstance(func, VidixyNodeBuilder):
            func = VidixyNodeBuilder(func)

        _, annotation = func.annotations.pop()
        func.controls.append(
            NodeControl(
                name=name,
                type=annotation.__name__,
                default=default,
                description=description,
            )
        )

        return func

    return wrapper


def output(name: str, socket: str, description: str = ""):
    """Add an output to a node."""

    def wrapper(
        func: Callable[P, T] | VidixyNodeBuilder[P, T]
    ) -> VidixyNodeBuilder[P, T]:
        if not isinstance(func, VidixyNodeBuilder):
            func = VidixyNodeBuilder(func)

        func.outputs.append(
            NodeOutput(name=name, socket=socket, description=description)
        )

        return func

    return wrapper


def load_nodes(dir: Path):
    """Load nodes from a directory."""
    sys.path.append(str(dir))

    for path in dir.rglob("*.py"):
        if path.stem.startswith("_"):
            continue

        module = path.relative_to(dir).with_suffix("").as_posix().replace("/", ".")
        importlib.import_module(module)


def normalize_name(name: str) -> str:
    """Normalize a name."""
    return name.replace("_", " ").title()


__all__ = [
    "VidixyNode",
    "node",
    "input",
    "control",
    "output",
    "load_nodes",
]

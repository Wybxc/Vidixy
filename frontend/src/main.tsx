import { createRoot } from 'react-dom/client'
import type { GetSchemes } from 'rete'
import { ClassicPreset, NodeEditor } from 'rete'
import { AreaPlugin } from 'rete-area-plugin'
import { ConnectionPlugin, Presets as ConnectionPresets } from 'rete-connection-plugin'
import type { ReactArea2D } from 'rete-react-render-plugin'
import { Presets, ReactRenderPlugin } from 'rete-react-render-plugin'
import type { ContextMenuExtra } from 'rete-context-menu-plugin'
import { ContextMenuPlugin, Presets as ContextMenuPresets } from 'rete-context-menu-plugin'

import './main.css'

type Schemes = GetSchemes<
  ClassicPreset.Node,
  ClassicPreset.Connection<ClassicPreset.Node, ClassicPreset.Node>
>
type AreaExtra = ReactArea2D<Schemes> | ContextMenuExtra<Schemes>

class NodeA extends ClassicPreset.Node {
  constructor(socket: ClassicPreset.Socket) {
    super('NodeA')
    this.addControl('port', new ClassicPreset.InputControl('text', {}))
    this.addOutput('port', new ClassicPreset.Output(socket))
  }
}

async function createEditor(container: HTMLElement): Promise<NodeEditor<Schemes>> {
  const editor = new NodeEditor<Schemes>()
  const area = new AreaPlugin<Schemes, AreaExtra>(container)
  editor.use(area)

  const socket = new ClassicPreset.Socket('text')
  const contextMenu = new ContextMenuPlugin<Schemes, AreaExtra>({
    items: ContextMenuPresets.classic.setup([['NodeA', () => new NodeA(socket)]])
  })
  area.use(contextMenu)

  const connection = new ConnectionPlugin<Schemes, AreaExtra>()
  connection.addPreset(ConnectionPresets.classic.setup())
  area.use(connection)

  const render = new ReactRenderPlugin<Schemes>({ createRoot })
  render.addPreset(Presets.classic.setup({ area }))
  render.addPreset(Presets.contextMenu.setup())
  area.use(render)

  return editor
}

const container = document.getElementById('container')
if (container === null) throw new Error('container not found')
createEditor(container)
  .then((editor) => {})
  .catch(console.error)

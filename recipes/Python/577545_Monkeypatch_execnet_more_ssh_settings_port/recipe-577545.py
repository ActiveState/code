#!/usr/bin/python
import execnet, execnet.gateway, execnet.multi
class SshPortGateway(execnet.gateway.SshGateway):
  def __init__(self, sshaddress, id, remotepython = None,
               ssh_config=None,
               ssh_port=None,
               ssh_identity=None,
               ssh_batchmode=None):
    self.remoteaddress = sshaddress
    if not remotepython: remotepython = "python"
    args = ['ssh', '-C' ]
    if ssh_config: args.extend(['-F', ssh_config])
    if ssh_port: args.extend(['-p', ssh_port])
    if ssh_identity: args.extend(['-i', ssh_identity])
    if ssh_batchmode: args.extend(["-o", "BatchMode yes"])
    remotecmd = '%s -c "%s"' % (remotepython, execnet.gateway.popen_bootstrapline)
    args.extend([sshaddress, remotecmd])
    execnet.gateway.PopenCmdGateway.__init__(self, args, id=id)
def makeportgateway(self, spec):
  spec = execnet.XSpec(spec)
  self.allocate_id(spec)
  gw = SshPortGateway(spec.ssh,
                      remotepython=spec.python,
                      ssh_config=spec.ssh_config,
                      id=spec.id,
                      ssh_port=spec.ssh_port,
                      ssh_identity=spec.ssh_identity,
                      ssh_batchmode=spec.ssh_batchmode)
  gw.spec = spec
  self._register(gw)
  # TODO add spec.{chdir,nice,env}
  return gw
execnet.multi.Group.makeportgateway = makeportgateway
execnet.makeportgateway = execnet.multi.default_group.makeportgateway

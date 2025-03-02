import fileinput

class MSBuild (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'msbuild', '15',  # note: fix scripts/ci/run-test-mac-sdk.sh when bumping the version number
			revision = 'de7a9c7b83f0cbfaedc0fc4cef3670755e0fc1f5')

	def build (self):
		try:
			self.sh ('./eng/cibuild_bootstrapped_msbuild.sh --host_type mono --configuration Release --skip_tests')
		finally:
			self.sh ('find artifacts stage1 -wholename \'*/log/*\' -type f -exec zip msbuild-bin-logs.zip {} \+')

	def install(self):
		# use the bootstrap msbuild as the system might not have one available!
		self.sh(
			f'./stage1/mono-msbuild/msbuild mono/build/install.proj /p:MonoInstallPrefix={self.staged_prefix} /p:Configuration=Release-MONO /p:IgnoreDiffFailure=true'
		)

MSBuild ()

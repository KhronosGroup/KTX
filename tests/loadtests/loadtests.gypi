##
# @internal
# @copyright © 2015, Mark Callow. For license see LICENSE.md.
#
# @brief Generate project file for building KTX loadtests.
#
{
  'includes': [
    '../../gyp_include/config.gypi',
    'appfwSDL/appfwSDL.gypi',
  ],
  'variables': { # level 1
    'variables': { # level 2 so can use in level 1
       # This is a list to avoid a very wide line.
       # -s is separate because '-s foo' in a list results
       # in "-s foo" on output.
       'additional_emcc_options': [
         '-s', 'ERROR_ON_UNDEFINED_SYMBOLS=1',
         '-s', 'TOTAL_MEMORY=52000000',
         '-s', 'NO_EXIT_RUNTIME=1',
       ],
       'testimages_dir': '../../testimages',
     }, # variables, level 2
     'data_files': [
        '<!@(ls <(testimages_dir)/*.ktx)',
     ],
    'datadir': 'testimages',
    'additional_emcc_options': [ '<@(additional_emcc_options)' ],
    'additional_emlink_options': [
      '<@(additional_emcc_options)',
      '-s', 'USE_SDL=2',
    ],
    # A hack to get INFOPLIST_FILE relativized. Keys ending in
    # _file & _dir assumed to be paths and are made relative to
    # the main .gyp file.
    'conditions': [
      ['OS == "ios"', {
        'infoplist_file': 'resources_ios/Info.plist',
      }, {
        'infoplist_file': 'resources_mac/Info.plist',
      }],
    ],
    'common_source_files': [
      'common/at.h',
      'common/at.c',
      'common/LoadTests.cpp',
      'common/LoadTests.h',
      'data/cube.h',
      'data/frame.h',
    ],
    'gl3_source_files': [
       # .h files are included so they will appear in IDEs' file lists.
      'shader-based/LoadTestsGL3.cpp',
      'shader-based/sample_01_draw_texture.c',
      'shader-based/sample_02_cube_textured.c',
      'shader-based/shaderfuncs.c',
      'shader-based/shaders.c',
    ],
  }, # variables, level 1

  'conditions': [
    ['OS == "mac" or OS == "win"', {
      'includes': [ '../../gyp_include/libgl.gypi' ],
      'targets': [
        {
          'target_name': 'gl3loadtests',
          'type': '<(executable)',
          'mac_bundle': 1,
          'dependencies': [
            'appfwSDL',
            'libktx.gl',
            'libgl',
          ],
          'sources': [
            '<@(common_source_files)',
            '<@(gl3_source_files)',
          ],
          'include_dirs': [
            'common',
          ],
          'defines': [
           'GL_CONTEXT_PROFILE=SDL_GL_CONTEXT_PROFILE_CORE',
           'GL_CONTEXT_MAJOR_VERSION=3',
           'GL_CONTEXT_MINOR_VERSION=3',
          ],
          'msvs_settings': {
            'VCLinkerTool': {
              # /SUBSYSTEM:WINDOWS.
              'SubSystem': '2',
            },
          },
          'xcode_settings': {
            'INFOPLIST_FILE': '<(infoplist_file)',
          },
          'conditions': [
            ['emit_emscripten_configs=="true"', {
              'configurations': {
                'Debug_Emscripten': {
                  'cflags': [ '<(additional_emcc_options)' ],
                  'ldflags': [
                    '--preload-files <(PRODUCT_DIR)/(datadir)@/<(datadir)',
                    '<(additional_emlink_options)',
                  ],
                  'msvs_settings': {
                    'VCCLCompilerTool': {
                      'AdditionalOptions': '<(additional_emcc_options)',
                    },
                    'VCLinkerTool': {
                      'PreloadFile': '<(PRODUCT_DIR)/<(datadir)@/<(datadir)',
                      'AdditionalOptions': '<(additional_emlink_options)',
                    },
                  },
                },
                'Release_Emscripten': {
                  'cflags': [ '<(additional_emcc_options)' ],
                  'ldflags': [
                    '--preload-files <(PRODUCT_DIR)/(datadir)@/<(datadir)',
                    '<(additional_emlink_options)',
                  ],
                  'msvs_settings': {
                    'VCCLCompilerTool': {
                      'AdditionalOptions': '<(additional_emcc_options)',
                    },
                    'VCLinkerTool': {
                      'PreloadFile': '<(PRODUCT_DIR)/<(datadir)@/<(datadir)',
                      'AdditionalOptions': '<(additional_emlink_options)',
                    },
                  },
                },
              },
            }], # emit_emscripten_configs=="true"
            ['OS == "win"', {
              'copies': [{
                'destination': '<(PRODUCT_DIR)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }],
            }], # OS == "win"
            ['OS == "mac"', {
              'copies': [{
                # A small change to GYP was required to use
                # UNLOCALIZED_RESOURCES_FOLDER_PATH.
                #'destination': '$(BUILT_PRODUCTS_DIR)/gl3loadtests.app/<(datadir)', # ios
                #'destination': '$(BUILT_PRODUCTS_DIR)/gl3loadtests.app/Resources/<(datadir)', # mac
                'destination': '$(UNLOCALIZED_RESOURCES_FOLDER_PATH)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }],
            }],
            ['OS == "android"', {
              #'includes': [ '../android_app_common.gypi' ],
              'copies': [{
                'destination': '<(android_assets_dir)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }], # copies
            }], # OS == "android"
          ], # conditions
        }, # gl3loadtests
      ], # 'OS == "mac" or OS == "win"' targets
    }], # 'OS == "mac" or OS == "win"'
    ['OS == "ios" or OS == "win"', {
      'includes': [
        '../../gyp_include/libgles3.gypi',
      ],
      'targets': [
        {
          'target_name': 'es3loadtests',
          'type': '<(executable)',
          'mac_bundle': 1,
          'dependencies': [
            'appfwSDL',
            'libktx.es3',
            'libgles3',
          ],
          #'toolsets': [target', 'emscripten'],
          'sources': [
            '<@(common_source_files)',
            'data/quad.h',
            '<@(gl3_source_files)',
          ], # sources
          'include_dirs': [
            'common',
          ],
          'defines': [
           'GL_CONTEXT_PROFILE=SDL_GL_CONTEXT_PROFILE_ES',
           'GL_CONTEXT_MAJOR_VERSION=3',
           'GL_CONTEXT_MINOR_VERSION=0',
          ],
          'msvs_settings': {
            'VCLinkerTool': {
              # /SUBSYSTEM:WINDOWS.
              'SubSystem': '2',
            },
          },
          'xcode_settings': {
            'INFOPLIST_FILE': '<(infoplist_file)',
          },
          'conditions': [
            ['OS == "ios"', {
              # Not needed for iOS simulator builds. I expect it is needed
              # for iOS device builds. Since I don't have code signing  I
              # can't complete a build to test.
              'mac_bundle_resources': [
                'resources_ios/Default.png',
                'resources_ios/Default-568h@2x.png',
                'resources_ios/Icon.png',
              ],
              'copies': [{
                # A small change to GYP was required to use
                # UNLOCALIZED_RESOURCES_FOLDER_PATH.
                #'destination': '$(BUILT_PRODUCTS_DIR)/es3loadtests.app/<(datadir)', # ios
                #'destination': '$(BUILT_PRODUCTS_DIR)/es3loadtests.app/Resources/<(datadir)', # mac
                'destination': '$(UNLOCALIZED_RESOURCES_FOLDER_PATH)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }],
            }], # OS == "ios"
            ['OS == "win"', {
              'copies': [{
                'destination': '<(PRODUCT_DIR)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }],
            }], # OS == "win"
          ],
        }, # es3loadtests
      ], # 'OS == "ios" or OS == "win"' targets
    }], # 'OS == "ios" or OS == "win"'
    ['OS == "ios" or (OS == "win" and es1support == "true")', {
      'includes': [
        '../../gyp_include/libgles1.gypi'
      ],
      'targets': [
        {
          'target_name': 'es1loadtests',
          'type': '<(executable)',
          'mac_bundle': 1,
          'dependencies': [
            'appfwSDL',
            'libktx.es1',
            'libgles1',
          ],
          #'toolsets': [target', 'emscripten'],
          'sources': [
            '<@(common_source_files)',
            'gles1/LoadTestsES1.cpp',
            'gles1/sample_01_draw_texture.c',
            'gles1/sample_02_cube_textured.c',
          ], # sources
          'include_dirs': [
            'common',
          ],
          'defines': [
            'GL_CONTEXT_PROFILE=SDL_GL_CONTEXT_PROFILE_ES',
            'GL_CONTEXT_MAJOR_VERSION=1',
            'GL_CONTEXT_MINOR_VERSION=1',
          ],
          'msvs_settings': {
            'VCLinkerTool': {
              # /SUBSYSTEM:WINDOWS.
              'SubSystem': '2',
            },
          },
          'xcode_settings': {
            'INFOPLIST_FILE': '<(infoplist_file)',
          },
          'conditions': [
            ['OS == "ios"', {
              # Not needed for iOS simulator builds. I expect it is needed
              # for iOS device builds. Since I don't have code signing  I
              # can't complete a build to test.
              'mac_bundle_resources': [
                'resources_ios/Default.png',
                'resources_ios/Default-568h@2x.png',
                'resources_ios/Icon.png',
              ],
              'copies': [{
                # A small change to GYP was required to use
                # UNLOCALIZED_RESOURCES_FOLDER_PATH.
                #'destination': '$(BUILT_PRODUCTS_DIR)/es1loadtests.app/<(datadir)', # ios
                #'destination': '$(BUILT_PRODUCTS_DIR)/es1loadtests.app/Resources/<(datadir)', # mac
                'destination': '$(UNLOCALIZED_RESOURCES_FOLDER_PATH)/<(datadir)',
                'files': [ '<@(data_files)' ],
              }],
            }], # OS == "ios"
            ], # conditions
        } # es1loadtests
      ], # 'OS == "ios" or OS == "win"' targets
    }] #'OS == "ios or OS == "win"'
  ], # conditions for conditional targets
}

# vim:ai:ts=4:sts=4:sw=2:expandtab:textwidth=70
